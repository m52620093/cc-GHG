from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SourceConfig:
    file_path: str
    sheet_name: str = "Sheet1"
    header_row: int = 12
    data_start_row: int = 13
    start_column: str = "C"
    end_column: str = "AI"
    columns: dict[str, str] = field(default_factory=dict)


@dataclass
class PatternPriorityConfig:
    rule: str = "numeric_desc"
    order: list[str] = field(default_factory=list)


@dataclass
class ImportConfig:
    template_file_path: str = "import_template.xlsx"
    sheet_name: str = "Sheet1"
    data_start_row: int = 2
    column_mapping: dict[str, str] = field(default_factory=dict)
    fixed_values: dict[str, object] = field(default_factory=dict)
    output_file_name: str = "import_{yyyyMMdd}.xlsx"


@dataclass
class NotificationConfig:
    interactive_mode: bool = True


@dataclass
class LogConfig:
    file_name: str = "error.log"
    max_bytes: int = 1_048_576
    backup_count: int = 5


@dataclass
class Settings:
    source: SourceConfig
    pattern_priority: PatternPriorityConfig
    import_: ImportConfig
    notification: NotificationConfig
    log: LogConfig


def load_settings(path: Path) -> Settings:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Settings(
        source=SourceConfig(**data["source"]),
        pattern_priority=PatternPriorityConfig(**data.get("pattern_priority", {})),
        import_=ImportConfig(**data["import"]),
        notification=NotificationConfig(**data.get("notification", {})),
        log=LogConfig(**data.get("log", {})),
    )
