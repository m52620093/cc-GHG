from __future__ import annotations

from .config import load_settings
from .import_writer import resolve_output_file_name, write_import_file
from .logging_setup import setup_logger
from .notify import show_message_box
from .paths import get_base_dir
from .selector import select_rows
from .source_reader import read_source_rows, validate_column_range

APP_TITLE = "GHGリスト取込処理"


def main() -> None:
    base_dir = get_base_dir()
    settings_path = base_dir / "setting.json"

    try:
        settings = load_settings(settings_path)
    except Exception as exc:
        show_message_box(APP_TITLE, f"setting.json の読み込みに失敗しました。\n{exc}", is_warning=True)
        return

    logger = setup_logger(base_dir, settings.log.file_name, settings.log.max_bytes, settings.log.backup_count)

    excluded_count = 0
    has_error = False

    try:
        for warning in validate_column_range(settings.source):
            logger.warning(warning)

        source_rows = read_source_rows(base_dir / settings.source.file_path, settings.source)
        result = select_rows(source_rows)
        excluded_count = result.excluded_count

        if excluded_count:
            logger.warning("GHG排出量単位毎が全パターンで空のため除外した部材図面: %d件", excluded_count)

        output_name = resolve_output_file_name(settings.import_.output_file_name)
        output_path = base_dir / output_name
        write_import_file(
            base_dir / settings.import_.template_file_path,
            output_path,
            settings.import_,
            result.rows,
        )
        logger.info(
            "処理完了: 出力件数=%d 除外件数=%d 出力ファイル=%s",
            len(result.rows),
            excluded_count,
            output_path.name,
        )
    except Exception:
        has_error = True
        logger.exception("処理中にエラーが発生しました")

    if settings.notification.interactive_mode:
        has_warning = has_error or excluded_count > 0
        lines = [f"除外件数: {excluded_count}件"]
        if has_warning:
            lines.append("エラー/警告が発生しました。error.log をご確認ください。")
        show_message_box(APP_TITLE, "\n".join(lines), is_warning=has_warning)
