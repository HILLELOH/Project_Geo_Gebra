"""Status bar — live tool / coordinates / shape count display."""
from __future__ import annotations
import tkinter as tk
from app.ui import styles

_TOOL_ICONS = {
    "Point":   "·",
    "Line":    "∕",
    "Segment": "—",
    "Circle":  "○",
    "Polygon": "⬠",
    "Delete":  "✕",
    "":        "◈",
}

_TOOL_COLORS = {
    "Point":   styles.SHAPE_COLOR["Point"],
    "Line":    styles.SHAPE_COLOR["Line"],
    "Segment": styles.SHAPE_COLOR["Segment"],
    "Circle":  styles.SHAPE_COLOR["Circle"],
    "Polygon": styles.SHAPE_COLOR["Polygon"],
    "Delete":  styles.EDIT_BTN_BG,
    "":        styles.TEXT_MUTED,
}


class StatusBar(tk.Frame):
    """Thin bar at the bottom of the window."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(
            parent,
            bg=styles.BG_BASE,
            height=styles.STATUS_HEIGHT,
        )
        self.pack_propagate(False)

        # Top divider (inside the bar so it doesn't need parent geometry tricks)
        tk.Frame(self, bg=styles.BORDER, height=1).pack(side=tk.TOP, fill=tk.X)

        # Left accent line
        tk.Frame(self, bg=styles.ACCENT_GLOW, width=1).pack(side=tk.LEFT, fill=tk.Y)

        # Tool indicator
        self._tool_icon = tk.Label(
            self, text="◈", font=styles.FONT_STATUS,
            bg=styles.BG_BASE, fg=styles.TEXT_MUTED,
            padx=8, pady=0,
        )
        self._tool_icon.pack(side=tk.LEFT)

        self._tool_label = tk.Label(
            self, text="Select a tool",
            font=styles.FONT_STATUS,
            bg=styles.BG_BASE, fg=styles.TEXT_MUTED,
            padx=0, pady=0,
        )
        self._tool_label.pack(side=tk.LEFT)

        # Separator
        tk.Frame(self, bg=styles.BORDER, width=1).pack(
            side=tk.LEFT, fill=tk.Y, padx=10, pady=4,
        )

        # Coordinates
        self._coords = tk.Label(
            self, text="x: —        y: —",
            font=styles.FONT_STATUS,
            bg=styles.BG_BASE, fg=styles.TEXT_DIM,
            padx=0, pady=0, width=24, anchor="w",
        )
        self._coords.pack(side=tk.LEFT)

        # Right: shape count
        self._count = tk.Label(
            self, text="0 shapes",
            font=styles.FONT_STATUS,
            bg=styles.BG_BASE, fg=styles.TEXT_MUTED,
            padx=12, pady=0,
        )
        self._count.pack(side=tk.RIGHT)

        # Right accent line
        tk.Frame(self, bg=styles.ACCENT_GLOW, width=1).pack(side=tk.RIGHT, fill=tk.Y)

    def set_tool(self, name: str) -> None:
        icon  = _TOOL_ICONS.get(name, "◈")
        color = _TOOL_COLORS.get(name, styles.TEXT_MUTED)
        self._tool_icon.configure(text=icon, fg=color)
        self._tool_label.configure(text=name if name else "Select a tool", fg=color)

    def set_coords(self, x: float, y: float) -> None:
        self._coords.configure(
            text=f"x: {x:+.3f}   y: {y:+.3f}",
            fg=styles.ACCENT_CYAN,
        )

    def clear_coords(self) -> None:
        self._coords.configure(text="x: —        y: —", fg=styles.TEXT_DIM)

    def update_count(self, n: int) -> None:
        self._count.configure(
            text=f"{n} shape{'s' if n != 1 else ''}",
            fg=styles.TEXT_MUTED if n == 0 else styles.TEXT,
        )
