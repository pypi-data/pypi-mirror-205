from __future__ import annotations

import sys
from pathlib import Path

from tukaan._tcl import Tcl
from tukaan._utils import reversed_dict


class Xcursor:
    loaded_cursors: dict[str, str] = {}
    defined_cursors: dict[str, str] = {}

    @staticmethod
    def init() -> None:
        Tcl.load_dll(
            Path(__file__).parent
            / "unix"
            / f"libtkxcursor_{'x64' if sys.maxsize > 2**32 else 'x32'}{Tcl.dll_ext}",
            "Xcursor",
        )

    @classmethod
    def load_cursor(cls, source: Path) -> str:
        source_str = Tcl.to(source)
        if source_str in cls.loaded_cursors.values():
            return reversed_dict(cls.loaded_cursors)[source_str]

        if not source.exists():
            raise FileNotFoundError(source)

        cursor_id = Tcl.call(str, "Xcursor::load_cursor_file", source_str)
        cls.loaded_cursors[cursor_id] = source_str
        return cursor_id

    @classmethod
    def set_cursor(cls, widget_name: str, cursor_id: str) -> None:
        Tcl.call(None, "Xcursor::set_cursor", widget_name, cursor_id)
        cls.defined_cursors[cursor_id] = widget_name

    @classmethod
    def cleanup_cursors(cls) -> None:
        for widget_name in cls.defined_cursors.values():
            Tcl.call(None, "Xcursor::undefine_cursor", widget_name)
        for cursor_id in cls.loaded_cursors:
            Tcl.call(None, "Xcursor::free_cursor", cursor_id)

        cls.loaded_cursors.clear()
        cls.defined_cursors.clear()
