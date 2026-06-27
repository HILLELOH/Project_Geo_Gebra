"""Undo / redo command history."""
from __future__ import annotations
import config
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle
from Shapes.Polygon import Polygon


def undo() -> None:
    if not config.undo_stack:
        return
    cmd = config.undo_stack.pop()
    _do_opposite(cmd)
    config.redo_stack.append(cmd)
    _refresh()


def redo() -> None:
    if not config.redo_stack:
        return
    cmd = config.redo_stack.pop()
    _do_same(cmd)
    config.undo_stack.append(cmd)
    _refresh()


def clear_history() -> None:
    config.undo_stack.clear()
    config.redo_stack.clear()


# ── internals ─────────────────────────────────────────────────────────────────

def _refresh() -> None:
    from app.canvas.renderer import update_display, update_label
    update_display()
    update_label()


def _rm(shape) -> None:
    if shape in config.shapes:
        config.shapes.remove(shape)


def _add(shape) -> None:
    """Add shape back to list without re-pushing to undo stack.
    update_display() in _refresh() will redraw it.
    """
    if shape not in config.shapes:
        config.shapes.append(shape)


def _do_same(cmd: dict) -> None:
    """Re-apply a command (redo path)."""
    from app.commands.operations import reset_canvas

    t     = cmd["type"]
    shape = cmd.get("shape")

    if t == "draw":
        if isinstance(shape, Point):
            _add(shape)
        elif isinstance(shape, (Line, Segment)):
            _add(shape.get_start())
            _add(shape.get_end())
            _add(shape)
        elif isinstance(shape, Circle):
            _add(shape.get_center())
            _add(shape)
        elif isinstance(shape, Polygon):
            for seg in shape.get_segment_list():
                _add(seg.get_start())
                _add(seg.get_end())
                _add(seg)
            _add(shape)

    elif t == "delete":
        if isinstance(shape, Point):
            _rm(shape)
        elif isinstance(shape, (Line, Segment)):
            _rm(shape.get_start())
            _rm(shape.get_end())
            _rm(shape)
        elif isinstance(shape, Circle):
            _rm(shape.get_center())
            _rm(shape)
        elif isinstance(shape, Polygon):
            for seg in shape.get_segment_list():
                _rm(seg.get_start())
                _rm(seg.get_end())
                _rm(seg)
            _rm(shape)

    elif t == "reset":
        reset_canvas()


def _do_opposite(cmd: dict) -> None:
    """Reverse a command (undo path)."""
    t     = cmd["type"]
    shape = cmd.get("shape")

    if t == "draw":
        if isinstance(shape, Point):
            _rm(shape)
        elif isinstance(shape, (Line, Segment)):
            _rm(shape.get_start())
            _rm(shape.get_end())
            _rm(shape)
        elif isinstance(shape, Circle):
            _rm(shape.get_center())
            _rm(shape)
        elif isinstance(shape, Polygon):
            for seg in shape.get_segment_list():
                _rm(seg.get_start())
                _rm(seg.get_end())
                _rm(seg)
            _rm(shape)

    elif t == "delete":
        if isinstance(shape, Point):
            _add(shape)
        elif isinstance(shape, (Line, Segment)):
            _add(shape.get_start())
            _add(shape.get_end())
            _add(shape)
        elif isinstance(shape, Circle):
            _add(shape.get_center())
            _add(shape)
        elif isinstance(shape, Polygon):
            for seg in shape.get_segment_list():
                _add(seg.get_start())
                _add(seg.get_end())
                _add(seg)
            _add(shape)

    elif t == "reset":
        config.shapes = list(cmd["list"])
