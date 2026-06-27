"""Canvas rendering — redraw shapes and rebuild the algebra panel."""
from __future__ import annotations
import re
import tkinter as tk
import matplotlib.pyplot as plt
import config
from app.ui import styles
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle
from Shapes.Polygon import Polygon


# ── public API ────────────────────────────────────────────────────────────────

def update_display() -> None:
    """Redraw all shapes, preserving the current view state."""
    ax = config.ax
    xlim   = ax.get_xlim()
    ylim   = ax.get_ylim()
    aspect = ax.get_aspect()
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()

    ax.cla()
    ax.set_facecolor(styles.CANVAS_BG)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_aspect(aspect)

    ax.grid(True, color=styles.CANVAS_GRID, linewidth=0.5, alpha=1.0, zorder=0)
    ax.axhline(0, color=styles.CANVAS_AXIS, linewidth=0.8, alpha=0.9, zorder=1)
    ax.axvline(0, color=styles.CANVAS_AXIS, linewidth=0.8, alpha=0.9, zorder=1)

    for sp in ax.spines.values():
        sp.set_color(styles.CANVAS_AXIS)
    ax.tick_params(colors=styles.TEXT_MUTED, labelcolor=styles.TEXT_MUTED, length=3)

    for shape in config.null_segments:
        shape.draw(ax)
    for shape in config.shapes:
        if not shape.is_hidden():
            shape.draw(ax)

    plt.draw()


def update_label() -> None:
    """Rebuild the algebra side-panel label list from the current shapes."""
    for widget in config.label_widgets:
        try:
            row = widget.master
            if row.winfo_exists():
                row.destroy()
        except tk.TclError:
            pass
    config.label_widgets = []

    seen: set = set()
    for shape in config.shapes:
        if id(shape) in seen:
            continue
        seen.add(id(shape))

        text = _format_label(shape)
        if text is None:
            continue

        shape_type = type(shape).__name__
        accent     = styles.SHAPE_COLOR.get(shape_type, styles.TEXT_MUTED)

        row = tk.Frame(config.side_panel.text, bg=styles.BG_SURFACE)
        row.pack(fill=tk.X, padx=4, pady=1)

        tk.Frame(row, bg=accent, width=3).pack(side=tk.LEFT, fill=tk.Y)

        widget = tk.Label(
            row,
            text=text,
            bg=styles.BG_SURFACE,
            fg=styles.TEXT,
            font=styles.FONT_MONO_SM,
            anchor="w",
            padx=8,
            pady=5,
            cursor="hand2",
        )
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Hover highlight
        def _enter(_, r=row, w=widget):
            r.configure(bg=styles.BG_HOVER)
            w.configure(bg=styles.BG_HOVER)

        def _leave(_, r=row, w=widget):
            r.configure(bg=styles.BG_SURFACE)
            w.configure(bg=styles.BG_SURFACE)

        widget.bind("<Enter>", _enter)
        widget.bind("<Leave>", _leave)
        widget.bind("<Button-3>", _on_right_click)
        widget.bind("<Button-1>", _on_left_click)

        config.label_widgets.append(widget)

    if config.status_bar:
        visible = sum(1 for s in config.shapes
                      if not isinstance(s, Polygon) and not _is_sub_shape(s))
        config.status_bar.update_count(len(config.shapes))


# ── helpers used by events.py ─────────────────────────────────────────────────

def get_shape_by_label(label: str):
    for shape in config.shapes:
        if shape.get_label() == label:
            return shape
    return None


def find_widget_by_shape(shape) -> tk.Label | None:
    target = shape.get_label()
    for widget in config.label_widgets:
        if _extract_label(widget) == target:
            return widget
    return None


# ── private ───────────────────────────────────────────────────────────────────

def _is_sub_shape(shape) -> bool:
    """True if shape is a point/segment that belongs to a compound shape."""
    if isinstance(shape, Point):
        return bool(
            shape.is_line_part(config.shapes)
            or shape.is_segment_part(config.shapes)
            or shape.is_circle_part(config.shapes)
            or shape.is_polygon_part(config.shapes)
        )
    return False


def _format_label(shape) -> str | None:
    eye = "◉" if not shape.is_hidden() else "◎"

    if isinstance(shape, Polygon):
        return f"{eye} ({shape.get_label()})  Polygon"

    if isinstance(shape, Line):
        m, b = shape.m_b()
        if m is None:
            return f"{eye} ({shape.get_label()})  x = {b}"
        if b is None:
            return f"{eye} ({shape.get_label()})  y = {m}"
        return f"{eye} ({shape.get_label()})  y = {m:.3f}x {b:+.3f}"

    if isinstance(shape, Segment):
        m, b = shape.m_b()
        if m is None:
            return f"{eye} ({shape.get_label()})  x = {b}"
        if b is None:
            return f"{eye} ({shape.get_label()})  y = {m}"
        return f"{eye} ({shape.get_label()})  y = {m:.3f}x {b:+.3f}"

    if isinstance(shape, Point):
        try:
            return (f"{eye} ({shape.get_label()})  "
                    f"({shape.get_x():.3f}, {shape.get_y():.3f})")
        except TypeError:
            return None

    if isinstance(shape, Circle):
        x = shape.get_center().get_x()
        y = shape.get_center().get_y()
        r = shape.get_radius()
        return (f"{eye} ({shape.get_label()})  "
                f"(x−{x:.2f})²+(y−{y:.2f})²={r**2:.2f}")

    return None


def _extract_label(widget: tk.Label) -> str | None:
    matches = re.findall(r"\((.*?)\)", widget.cget("text"))
    return matches[0] if matches else None


def _on_left_click(event) -> None:
    """Highlight shape when its algebra-panel label is left-clicked."""
    update_display()
    widget: tk.Label = event.widget

    if config.last_shape is not None:
        w = find_widget_by_shape(config.last_shape)
        if w:
            w.configure(fg=styles.TEXT)

    label = _extract_label(widget)
    if not label:
        return
    shape = get_shape_by_label(label)
    if not shape:
        return

    shape.set_color("cyan")
    widget.configure(fg=styles.ACCENT_CYAN)
    config.last_widget = widget
    config.last_shape  = shape
    plt.draw()


def _on_right_click(event) -> None:
    """Toggle shape visibility on right-click in the algebra panel."""
    label = _extract_label(event.widget)
    if not label:
        return
    shape = get_shape_by_label(label)
    if not shape:
        return
    _toggle_hidden(shape)
    update_display()
    update_label()


def _toggle_hidden(shape) -> None:
    if isinstance(shape, Point):
        shape.set_hidden(not shape.is_hidden())
    elif isinstance(shape, (Line, Segment)):
        hide = not shape.is_hidden()
        shape.get_start().set_hidden(hide)
        shape.get_end().set_hidden(hide)
        shape.set_hidden(hide)
    elif isinstance(shape, Circle):
        hide = not shape.is_hidden()
        shape.get_center().set_hidden(hide)
        shape.set_hidden(hide)
