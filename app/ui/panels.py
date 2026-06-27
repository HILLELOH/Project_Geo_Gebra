"""Panel widgets — dark-themed algebra panel and algorithm panel."""
from __future__ import annotations
import sys
import tkinter as tk
from tkinter import ttk
from app.ui import styles


class AlgebraPanel(tk.Frame):
    """Dark scrollable panel for the algebra view (left side).

    self.text — the inner scrollable tk.Frame; pack widgets directly into it.
    """

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=styles.BG_PANEL, width=styles.PANEL_WIDTH)
        self.pack_propagate(False)

        self._build_header()
        self._build_scroll_area()

    def _build_header(self) -> None:
        hdr = tk.Frame(self, bg=styles.BG_PANEL)
        hdr.pack(fill=tk.X)

        tk.Label(
            hdr, text="ALGEBRA",
            bg=styles.BG_PANEL, fg=styles.ACCENT_BLUE,
            font=styles.FONT_HEADING, padx=12, pady=10, anchor="w",
        ).pack(side=tk.LEFT)

        tk.Frame(self, bg=styles.ACCENT_BLUE, height=1).pack(fill=tk.X)

    def _build_scroll_area(self) -> None:
        area = tk.Frame(self, bg=styles.BG_PANEL)
        area.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(
            area, bg=styles.BG_PANEL,
            highlightthickness=0, bd=0,
        )
        sb = ttk.Scrollbar(area, orient="vertical", command=self._canvas.yview)

        self.text = tk.Frame(self._canvas, bg=styles.BG_PANEL)
        self._win_id = self._canvas.create_window((0, 0), window=self.text, anchor="nw")

        self._canvas.configure(yscrollcommand=sb.set)
        self.text.bind("<Configure>", self._on_inner_resize)
        self._canvas.bind("<Configure>", self._on_canvas_resize)

        for widget in (self._canvas, self.text):
            widget.bind("<MouseWheel>", self._on_mousewheel)
            if sys.platform != "darwin":
                widget.bind("<Button-4>", lambda e: self._canvas.yview_scroll(-1, "units"))
                widget.bind("<Button-5>", lambda e: self._canvas.yview_scroll(1, "units"))

        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _on_inner_resize(self, event=None) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._win_id, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        delta = int(-1 * event.delta) if sys.platform == "darwin" else int(-1 * (event.delta / 120))
        self._canvas.yview_scroll(delta, "units")


class SidePanel(tk.Frame):
    """Dark text panel used by the algorithms side panel.

    Provides insert_text / insert_block / clear_text on a tk.Text widget.
    Widgets can also be packed into self.text as a container.
    """

    def __init__(
        self,
        parent: tk.Widget,
        scrollable: bool = True,
        pack_side: str = tk.LEFT,
        pack_text: bool = True,
    ) -> None:
        super().__init__(parent, bg=styles.BG_PANEL, bd=0)
        self.text = tk.Text(
            self,
            wrap=tk.WORD,
            font=styles.FONT_MONO_SM,
            bg=styles.BG_PANEL,
            fg=styles.TEXT,
            insertbackground=styles.TEXT,
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=6,
            cursor="arrow",
            selectbackground=styles.BG_ACTIVE,
            selectforeground=styles.TEXT,
        )
        self.text.configure(state="disabled")

        if pack_text:
            self.text.pack(side=pack_side, fill=tk.BOTH, expand=True)

        if scrollable:
            sb = ttk.Scrollbar(self, command=self.text.yview)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            self.text.config(yscrollcommand=sb.set)

    def insert_text(self, text: str) -> None:
        self.text.configure(state="normal")
        self.text.insert(tk.END, text)
        self.text.configure(state="disabled")

    def insert_block(self, texts: list) -> None:
        for t in texts:
            self.insert_text(t)

    def clear_text(self) -> None:
        self.text.configure(state="normal")
        self.text.delete(1.0, tk.END)
        self.text.configure(state="disabled")
