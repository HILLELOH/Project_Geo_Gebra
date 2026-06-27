"""File save and load operations (pickle format)."""
from __future__ import annotations
import pickle
from tkinter import filedialog
import config
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle


def save() -> None:
    path = filedialog.asksaveasfilename(
        defaultextension=".p",
        filetypes=[("PyGeoGebra Files", "*.p")],
    )
    if not path:
        return
    with open(path, "wb") as f:
        pickle.dump([{"shape": s} for s in config.shapes], f)


def load() -> None:
    path = filedialog.askopenfilename(filetypes=[("PyGeoGebra Files", "*.p")])
    if not path:
        return

    from app.commands.operations import draw_shape, reset_canvas
    reset_canvas()

    with open(path, "rb") as f:
        records = pickle.load(f)

    shapes = [r["shape"] for r in records]

    for shape in shapes:
        if isinstance(shape, (Line, Segment)):
            draw_shape(shape.get_start()); config.undo_stack.pop()
            draw_shape(shape.get_end());   config.undo_stack.pop()
            draw_shape(shape);             config.undo_stack.pop()
        elif isinstance(shape, Circle):
            draw_shape(shape.get_center()); config.undo_stack.pop()
            draw_shape(shape);              config.undo_stack.pop()
        elif isinstance(shape, Point):
            if (not shape.is_line_part(shapes)
                    and not shape.is_circle_part(shapes)
                    and not shape.is_segment_part(shapes)):
                draw_shape(shape)
                config.undo_stack.pop()
