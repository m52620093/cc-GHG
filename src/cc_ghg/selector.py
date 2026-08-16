from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from .source_reader import SourceRow

_PATTERN_NUMBER_RE = re.compile(r"\d+")


@dataclass
class SelectedRow:
    part_drawing: str
    ghg_per_unit: float


@dataclass
class SelectionResult:
    rows: list[SelectedRow]
    excluded_count: int


def _pattern_priority(pattern: str) -> int:
    match = _PATTERN_NUMBER_RE.search(pattern)
    return int(match.group()) if match else -1


def _registered_at_key(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    if value:
        try:
            return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
    return datetime.min


def select_rows(rows: list[SourceRow]) -> SelectionResult:
    """部材図面ごとにグルーピングし、優先順位に従って採用する1行を決定する。

    優先順位: GHG排出量算定パターンの数値部分が大きいものを優先し、
    同一パターン内では登録日時が新しいものを優先する。
    優先順位が最も高い候補から順に見て、GHG排出量単位毎に値がある最初の行を採用する。
    """
    groups: dict[str, list[SourceRow]] = defaultdict(list)
    for row in rows:
        if row.part_drawing:
            groups[row.part_drawing].append(row)

    selected: list[SelectedRow] = []
    excluded_count = 0

    for part_drawing, candidates in groups.items():
        candidates.sort(
            key=lambda r: (_pattern_priority(r.pattern), _registered_at_key(r.registered_at)),
            reverse=True,
        )
        chosen = next((c for c in candidates if c.ghg_per_unit is not None), None)
        if chosen is None:
            excluded_count += 1
            continue
        selected.append(
            SelectedRow(
                part_drawing=part_drawing,
                ghg_per_unit=chosen.ghg_per_unit,
            )
        )

    return SelectionResult(rows=selected, excluded_count=excluded_count)
