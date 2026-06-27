"""PyGeoGebra — application entry point."""
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from label_generator import generate_alphanumeric_sequence
from app.ui import styles
from app.ui.panels import AlgebraPanel
from app.ui.toolbar import create_toolbar
from app.ui.status_bar import StatusBar
from app.canvas.events import (
    connect_events,
    activate_draw_point, activate_draw_line, activate_draw_segment,
    activate_draw_circle, activate_draw_polygon, activate_delete,
)
from app.canvas.renderer import update_display
from app.commands.operations import reset_canvas
from app.commands.history import undo, redo, clear_history
from app.io.persistence import save, load
from app.ui.algo_panel import toggle_algo_panel
from app.ui.dialogs import open_info_window


def main() -> None:
    config.root = tk.Tk()
    config.root.configure(bg=styles.BG_BASE)

    config.fig, config.ax = plt.subplots(facecolor=styles.BG_BASE)
    config.fig.patch.set_facecolor(styles.BG_BASE)
    config.label_generator = generate_alphanumeric_sequence()

    _init_window()
    _init_layout()
    connect_events()
    config.root.protocol("WM_DELETE_WINDOW", _on_closing)
    update_display()
    config.root.mainloop()


def _init_window() -> None:
    w = config.root.winfo_screenwidth()
    h = config.root.winfo_screenheight()
    config.root.geometry(f"{w}x{h}")
    config.root.wm_title("PyGeoGebra")

    ax = config.ax
    config.fig.set_size_inches(8, 8)
    ax.set_facecolor(styles.CANVAS_BG)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect("equal")
    ax.grid(True, color=styles.CANVAS_GRID, linewidth=0.5, alpha=1.0)
    ax.set_xticks(np.arange(-20, 21, 5))
    ax.set_yticks(np.arange(-20, 21, 5))
    ax.axhline(0, color=styles.CANVAS_AXIS, linewidth=0.8, alpha=0.9)
    ax.axvline(0, color=styles.CANVAS_AXIS, linewidth=0.8, alpha=0.9)

    for sp in ax.spines.values():
        sp.set_color(styles.CANVAS_AXIS)
    ax.tick_params(colors=styles.TEXT_MUTED, labelcolor=styles.TEXT_MUTED, length=3)


def _init_layout() -> None:
    # ── toolbar (top) ─────────────────────────────────────────────────────────
    config.buttons_panel = tk.Frame(config.root, bg=styles.BG_BASE)
    config.buttons_panel.pack(side=tk.TOP, fill=tk.X)

    tk.Frame(config.root, bg=styles.BORDER, height=1).pack(
        side=tk.TOP, fill=tk.X
    )

    create_toolbar(
        config.buttons_panel,
        draw_point    = activate_draw_point,
        draw_line     = activate_draw_line,
        draw_segment  = activate_draw_segment,
        draw_circle   = activate_draw_circle,
        draw_polygon  = activate_draw_polygon,
        reset         = reset_canvas,
        save          = save,
        load          = load,
        delete        = activate_delete,
        algos         = toggle_algo_panel,
        undo          = undo,
        redo          = redo,
        clear_history = clear_history,
        info          = open_info_window,
    )

    # ── status bar (bottom) ───────────────────────────────────────────────────
    config.status_bar = StatusBar(config.root)
    config.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ── algebra side panel (left) ─────────────────────────────────────────────
    config.side_panel = AlgebraPanel(config.root)
    config.side_panel.pack(side=tk.LEFT, fill=tk.Y)

    tk.Frame(config.root, bg=styles.BORDER, width=1).pack(
        side=tk.LEFT, fill=tk.Y
    )

    # ── matplotlib canvas (fills remaining space) ─────────────────────────────
    config.canvas = FigureCanvasTkAgg(config.fig, master=config.root)
    config.canvas.get_tk_widget().configure(bg=styles.BG_BASE, highlightthickness=0)
    config.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    config.shapes        = []
    config.label_widgets = []


def _on_closing() -> None:
    if messagebox.askyesno("Quit", "Save before closing?",
                           icon="question",
                           parent=config.root):
        save()
    config.root.quit()
    config.root.destroy()


if __name__ == "__main__":
    main()
