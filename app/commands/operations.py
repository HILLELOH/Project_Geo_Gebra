"""Drawing and deletion operations — the core mutation layer."""
from __future__ import annotations
import logging
import numpy as np
import matplotlib.pyplot as plt
import config
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle
from Shapes.Polygon import Polygon
from label_generator import get_label_parts, generate_alphanumeric_sequence

log = logging.getLogger(__name__)


# ── public API ────────────────────────────────────────────────────────────────

def draw_shape(shape) -> None:
    """Draw *shape*, add it to the shapes list, and push a draw command to the undo stack."""
    chars, numbers = get_label_parts(shape.get_label())
    config.last_label_before_return = chars
    config.last_turn_before_return = numbers

    shape.draw(config.ax)
    config.shapes.append(shape)
    config.undo_stack.append({"type": "draw", "shape": shape})
    config.redo_stack.clear()          # new action invalidates redo history

    from app.canvas.renderer import update_display, update_label
    update_display()
    update_label()


def delete_by_label(label: str) -> None:
    """Delete a shape (and its dependent components) identified by *label*."""
    shape = _find(label)
    if shape is None:
        return

    if isinstance(shape, Point):
        _delete_point(shape)
    elif isinstance(shape, Line):
        _delete_line(shape)
    elif isinstance(shape, Segment):
        _delete_segment(shape)
    elif isinstance(shape, Circle):
        _delete_circle(shape)

    config.redo_stack.clear()          # new action invalidates redo history

    from app.canvas.renderer import update_display, update_label
    update_display()
    update_label()


def move_shape(shape, dx: float, dy: float) -> None:
    """Translate *shape* by (dx, dy) and refresh the view."""
    if isinstance(shape, Point):
        shape.coords[0][0] += dx
        shape.coords[0][1] += dy
        shape.set_x(dx)
        shape.set_y(dy)
    elif isinstance(shape, Circle):
        c = shape.get_center()
        c.coords[0][0] += dx
        c.coords[0][1] += dy
        shape.set_center(dx, dy)
    elif isinstance(shape, (Line, Segment)):
        for pt in (shape.get_start(), shape.get_end()):
            pt.coords[0][0] += dx
            pt.coords[0][1] += dy
        shape.set_start_point(dx, dy)
        shape.set_end_point(dx, dy)

    from app.canvas.renderer import update_display, update_label
    update_display()
    update_label()
    plt.draw()


def reset_canvas() -> None:
    """Clear all shapes and reset the canvas to its initial state."""
    from app.ui import styles

    config.undo_stack.append({"type": "reset", "list": list(config.shapes)})
    config.redo_stack.clear()
    _clean_null_segments()

    config.ax.clear()
    config.shapes        = []
    config.null_segments = []
    config.deleted_labels = []

    for widget in config.label_widgets:
        try:
            row = widget.master
            if row.winfo_exists():
                row.destroy()
        except Exception:
            pass
    config.label_widgets = []

    config.label_generator = generate_alphanumeric_sequence()

    ax = config.ax
    ax.set_facecolor(styles.CANVAS_BG)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect("equal")
    ax.grid(True, color=styles.CANVAS_GRID, linewidth=0.5)
    ax.set_xticks(np.arange(-20, 21, 5))
    ax.set_yticks(np.arange(-20, 21, 5))
    ax.axhline(0, color=styles.CANVAS_AXIS, linewidth=0.8)
    ax.axvline(0, color=styles.CANVAS_AXIS, linewidth=0.8)
    for sp in ax.spines.values():
        sp.set_color(styles.CANVAS_AXIS)
    ax.tick_params(colors=styles.TEXT_MUTED, labelcolor=styles.TEXT_MUTED, length=3)
    plt.draw()

    if config.bool_panel_algo:
        from app.ui.algo_panel import toggle_algo_panel
        toggle_algo_panel()
        toggle_algo_panel()


# ── internal helpers ──────────────────────────────────────────────────────────

def _find(label: str):
    for s in config.shapes:
        if s.get_label() == label:
            return s
    return None


def _remove(shape) -> None:
    if shape in config.shapes:
        config.shapes.remove(shape)


def _record(label: str) -> None:
    config.deleted_labels.append(label)


def _push_delete(shape) -> None:
    config.undo_stack.append({"type": "delete", "shape": shape})


def _delete_point(point: Point) -> None:
    poly = point.is_polygon_part()
    if poly:
        _delete_polygon(poly)
        return

    line = point.is_line_part()
    seg  = point.is_segment_part()
    circ = point.is_circle_part()

    if line:
        log.debug("delete point → line")
        _remove(line.get_start()); _remove(line.get_end()); _remove(line)
        for s in (line.get_start(), line.get_end(), line):
            _record(s.get_label())
        _push_delete(line)
    elif seg:
        log.debug("delete point → segment")
        _remove(seg.get_start()); _remove(seg.get_end()); _remove(seg)
        for s in (seg.get_start(), seg.get_end(), seg):
            _record(s.get_label())
        _push_delete(seg)
    elif circ:
        log.debug("delete point → circle")
        _remove(circ.get_center()); _remove(circ)
        _record(circ.get_center().get_label()); _record(circ.get_label())
        _push_delete(circ)
    else:
        _remove(point)
        _record(point.get_label())
        _push_delete(point)


def _delete_line(line: Line) -> None:
    _remove(line.get_start()); _remove(line.get_end()); _remove(line)
    for s in (line.get_start(), line.get_end(), line):
        _record(s.get_label())
    _push_delete(line)


def _delete_segment(seg: Segment) -> None:
    for s in config.shapes:
        if isinstance(s, Polygon) and seg in s.get_segment_list():
            _delete_polygon(s)
            return
    _remove(seg.get_start()); _remove(seg.get_end()); _remove(seg)
    for s in (seg.get_start(), seg.get_end(), seg):
        _record(s.get_label())
    _push_delete(seg)


def _delete_circle(circ: Circle) -> None:
    _remove(circ.get_center()); _remove(circ)
    _record(circ.get_center().get_label()); _record(circ.get_label())
    _push_delete(circ)


def _delete_polygon(poly: Polygon) -> None:
    for seg in poly.get_segment_list():
        _remove(seg.get_start())
        _remove(seg.get_end())
        _remove(seg)
    _remove(poly)


def _clean_null_segments() -> None:
    config.shapes = [
        s for s in config.shapes
        if not (isinstance(s, Segment) and s.get_label() == "")
    ]
