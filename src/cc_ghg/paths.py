from __future__ import annotations

import sys
from pathlib import Path


def get_base_dir() -> Path:
    """設定ファイル・入出力ファイルを探すための基準ディレクトリを返す。

    exe化後はexe自身のフォルダ、開発時(uv run)はカレントディレクトリを基準にする。
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()
