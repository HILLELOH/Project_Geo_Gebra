"""Toolbar — flat label-based buttons with hover/active effects."""
from __future__ import annotations
import tkinter as tk
from app.ui import styles


class FlatButton(tk.Label):
    """tk.Label styled as a flat toolbar button with hover/active state."""

    def __init__(
        self,
        parent: tk.Widget,
        *,
        text: str,
        command,
        group: str,
    ) -> None:
        g = styles.group(group)
        super().__init__(
            parent,
            text=text,
            bg=g["bg"],
            fg=g["fg"],
            font=styles.FONT_UI,
            padx=14,
            pady=0,
            cursor="hand2",
            anchor="center",
        )
        self._cmd    = command
        self._bg     = g["bg"]
        self._hover  = g["hover"]
        self._active = g["active"]

        self.bind("<Enter>",          self._on_enter)
        self.bind("<Leave>",          self._on_leave)
        self.bind("<Button-1>",       self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _=None)  -> None: self.configure(bg=self._hover)
    def _on_leave(self, _=None)  -> None: self.configure(bg=self._bg)
    def _on_press(self, _=None)  -> None: self.configure(bg=self._active)

    def _on_release(self, _=None) -> None:
        self.configure(bg=self._bg)
        if self._cmd:
            self._cmd()


def _sep(panel: tk.Frame) -> None:
    tk.Frame(panel, bg=styles.BORDER_LIGHT, width=1).pack(
        side=tk.LEFT, fill=tk.Y, padx=5, pady=6,
    )


def _btn(panel: tk.Frame, text: str, cmd, group: str, side: str = tk.LEFT) -> None:
    FlatButton(panel, text=text, command=cmd, group=group).pack(
        side=side, padx=1, fill=tk.Y,
    )


def create_toolbar(
    panel: tk.Frame,
    *,
    draw_point, draw_line, draw_segment, draw_circle, draw_polygon,
    reset, save, load, delete,
    algos, undo, redo, clear_history, info,
) -> None:
    """Populate *panel* with colour-grouped flat buttons."""
    panel.configure(bg=styles.BG_BASE, height=styles.TOOLBAR_HEIGHT)
    panel.pack_propagate(False)

    # ── file ──────────────────────────────────────────────────────────────────
    _btn(panel, "💾 Save", save, "file")
    _btn(panel, "📂 Load", load, "file")
    _sep(panel)

    # ── drawing tools ─────────────────────────────────────────────────────────
    _btn(panel, "· Point",   draw_point,   "draw")
    _btn(panel, "∕ Line",    draw_line,    "draw")
    _btn(panel, "― Segment", draw_segment, "draw")
    _btn(panel, "○ Circle",  draw_circle,  "draw")
    _btn(panel, "⬠ Polygon", draw_polygon, "draw")
    _sep(panel)

    # ── edit ──────────────────────────────────────────────────────────────────
    _btn(panel, "✕ Delete", delete, "edit")
    _btn(panel, "↺ Reset",  reset,  "edit")
    _sep(panel)

    # ── algorithms ────────────────────────────────────────────────────────────
    _btn(panel, "⚙ Algorithms", algos, "algo")

    # ── right-aligned ─────────────────────────────────────────────────────────
    _btn(panel, "ℹ Info",       info,          "info",    tk.RIGHT)
    _sep(panel)
    _btn(panel, "↷ Redo",       redo,          "history", tk.RIGHT)
    _btn(panel, "↶ Undo",       undo,          "history", tk.RIGHT)
    _btn(panel, "⊘ Hist",       clear_history, "history", tk.RIGHT)
