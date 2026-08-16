from __future__ import annotations

import ctypes

_MB_OK = 0x0
_MB_ICONWARNING = 0x30
_MB_ICONINFORMATION = 0x40


def show_message_box(title: str, message: str, is_warning: bool = False) -> None:
    icon = _MB_ICONWARNING if is_warning else _MB_ICONINFORMATION
    ctypes.windll.user32.MessageBoxW(0, message, title, _MB_OK | icon)
