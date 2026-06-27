"""Algorithms side panel — proper layout with separate results area."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import config
from Shapes.Polygon import Polygon
from app.ui import styles


def toggle_algo_panel() -> None:
    if config.bool_panel_algo:
        config.algorithms_panel.pack_forget()
        config.bool_panel_algo = False
    else:
        _build_panel()


def refresh_shape_dropdown() -> None:
    if config.bool_panel_algo and config.menu is not None:
        _update_shape_options()


def _build_panel() -> None:
    config.calc = False

    # ── outer container (replaces SidePanel) ──────────────────────────────────
    container = tk.Frame(config.root, bg=styles.BG_PANEL, width=240)
    container.pack(side=tk.RIGHT, fill=tk.Y)
    container.pack_propagate(False)
    config.algorithms_panel = container
    config.bool_panel_algo = True

    # ── header ────────────────────────────────────────────────────────────────
    tk.Label(
        container, text="ALGORITHMS",
        bg=styles.BG_PANEL, fg=styles.ALGO_BTN_BG,
        font=styles.FONT_HEADING, padx=12, pady=10, anchor="w",
    ).pack(fill=tk.X)
    tk.Frame(container, bg=styles.ALGO_BTN_BG, height=1).pack(fill=tk.X)

    # ── controls ──────────────────────────────────────────────────────────────
    ctrl = tk.Frame(container, bg=styles.BG_PANEL)
    ctrl.pack(fill=tk.X, padx=12, pady=8)

    tk.Label(ctrl, text="Algorithm", font=styles.FONT_UI,
             bg=styles.BG_PANEL, fg=styles.TEXT_MUTED, anchor="w").pack(anchor="w")
    config.algo_var = tk.StringVar(value="choose")
    config.algo_var.trace_add("write", lambda *_: _update_shape_options())
    _dark_menu(ctrl, config.algo_var,
               "choose", "Perimeter", "Area", "Convex-hull", "Triangulation"
               ).pack(anchor="w", pady=(2, 10), fill=tk.X)

    tk.Label(ctrl, text="Shape", font=styles.FONT_UI,
             bg=styles.BG_PANEL, fg=styles.TEXT_MUTED, anchor="w").pack(anchor="w")
    config.poly_var = tk.StringVar(value="choose")
    shape_labels = ["choose"] + [s.get_label() for s in config.shapes]
    shape_menu = _dark_menu(ctrl, config.poly_var, *shape_labels)
    shape_menu.pack(anchor="w", pady=(2, 10), fill=tk.X)
    config.menu = shape_menu

    tk.Frame(container, bg=styles.BORDER, height=1).pack(fill=tk.X, padx=8)

    btn = tk.Frame(container, bg=styles.BG_PANEL)
    btn.pack(fill=tk.X, padx=12, pady=8)
    tk.Button(btn, text="Calculate", command=_activate,
              **styles.btn_kw(styles.ALGO_BTN_BG)).pack(fill=tk.X, pady=2)
    tk.Button(btn, text="Reset", command=_reset_algo,
              **styles.btn_kw(styles.EDIT_BTN_BG)).pack(fill=tk.X)

    tk.Frame(container, bg=styles.BORDER, height=1).pack(fill=tk.X, padx=8, pady=(4, 0))

    # ── results text area ─────────────────────────────────────────────────────
    results = tk.Text(
        container,
        bg=styles.BG_SURFACE, fg=styles.TEXT,
        font=styles.FONT_MONO_SM,
        relief="flat", bd=0,
        padx=10, pady=8,
        state="disabled",
        wrap="word",
        cursor="arrow",
        selectbackground=styles.BG_ACTIVE,
    )
    results.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
    container._results = results

    # Attach text methods to container for backward compat
    def _clear():
        results.configure(state="normal")
        results.delete(1.0, tk.END)
        results.configure(state="disabled")

    def _insert(text):
        results.configure(state="normal")
        results.insert(tk.END, text)
        results.configure(state="disabled")

    container.clear_text   = _clear
    container.insert_text  = _insert
    container.insert_block = lambda texts: [_insert(t) for t in texts]


def _dark_menu(parent, var, *values) -> tk.OptionMenu:
    m = tk.OptionMenu(parent, var, *values)
    m.configure(
        bg=styles.BG_SURFACE, fg=styles.TEXT,
        activebackground=styles.BG_HOVER, activeforeground=styles.TEXT,
        highlightthickness=0, relief="flat", font=styles.FONT_UI,
        anchor="w",
    )
    m["menu"].configure(
        bg=styles.BG_SURFACE, fg=styles.TEXT,
        activebackground=styles.BG_ACTIVE, activeforeground=styles.TEXT,
        font=styles.FONT_UI,
    )
    return m


def _update_shape_options() -> None:
    if config.menu is None:
        return
    algo = config.algo_var.get() if config.algo_var else "choose"
    if algo in ("Convex-hull", "Triangulation"):
        labels = [s.get_label() for s in config.shapes if isinstance(s, Polygon)]
    else:
        labels = [s.get_label() for s in config.shapes]

    config.menu["menu"].delete(0, "end")
    for label in labels:
        config.menu["menu"].add_command(
            label=label,
            command=lambda opt=label: config.poly_var.set(opt),
        )


def _activate() -> None:
    from app.algorithms import find_shape, run_convex_hull, run_triangulation
    from app.canvas.renderer import update_display

    if not config.bool_panel_algo:
        return

    update_display()
    config.algorithms_panel.clear_text()

    algo        = config.algo_var.get()
    shape_label = config.poly_var.get()
    if algo == "choose" or shape_label == "choose":
        config.algorithms_panel.insert_text("Select an algorithm and shape.")
        return

    shape = find_shape(shape_label)
    if shape is None:
        config.algorithms_panel.insert_text(f"Shape '{shape_label}' not found.")
        return

    _show_shape_info(shape)

    if algo == "Perimeter":
        config.algorithms_panel.insert_text(f"\nPerimeter:  {shape.perimeter():.4f}\n")
    elif algo == "Area":
        config.algorithms_panel.insert_text(f"\nArea:  {shape.area():.4f}\n")
    elif algo == "Convex-hull":
        vertices = run_convex_hull(shape_label)
        config.algorithms_panel.insert_text(f"\nConvex Hull vertices:\n  {vertices}\n")
        update_display()
    elif algo == "Triangulation":
        run_triangulation(shape_label)
        update_display()


def _show_shape_info(shape) -> None:
    from Shapes.Point import Point
    from Shapes.Line import Line
    from Shapes.Segment import Segment
    from Shapes.Circle import Circle

    p = config.algorithms_panel
    p.insert_block([
        f"Type:   {type(shape).__name__}\n",
        f"Label:  {shape.get_label()}\n",
    ])
    if isinstance(shape, Point):
        p.insert_text(f"Coords: ({shape.get_x():.3f}, {shape.get_y():.3f})\n")
    elif isinstance(shape, Circle):
        c = shape.get_center()
        p.insert_block([
            f"Center: ({c.get_x():.3f}, {c.get_y():.3f})\n",
            f"Radius: {shape.get_radius():.3f}\n",
        ])
    elif isinstance(shape, (Line, Segment)):
        p.insert_block([
            f"Start:  ({shape.get_start().get_x():.3f}, {shape.get_start().get_y():.3f})\n",
            f"End:    ({shape.get_end().get_x():.3f}, {shape.get_end().get_y():.3f})\n",
        ])


def _reset_algo() -> None:
    config.null_segments = []
    if config.bool_panel_algo and config.algorithms_panel is not None:
        config.algorithms_panel.pack_forget()
        config.bool_panel_algo = False
    _build_panel()
