"""Matplotlib canvas event handlers and drawing-tool activators."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import config
from app.ui import styles
from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle
from Shapes.Polygon import Polygon
from app.canvas.renderer import update_display, update_label, find_widget_by_shape


# ── connection ────────────────────────────────────────────────────────────────

def connect_events() -> None:
    cv = config.ax.figure.canvas
    config.press_cid   = cv.mpl_connect("button_press_event",   on_press)
    config.release_cid = cv.mpl_connect("button_release_event", on_release)
    config.motion_cid  = cv.mpl_connect("motion_notify_event",  on_motion)
    cv.mpl_connect("scroll_event",    on_scroll)
    cv.mpl_connect("key_press_event", on_key)
    cv.mpl_connect("axes_leave_event", on_axes_leave)


# ── tool activators ───────────────────────────────────────────────────────────

def _reset_tool_cid() -> None:
    if config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)
        config.cid = None
    if config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
        config.circle_cid = None


def _set_tool(name: str) -> None:
    config.active_tool = name
    if config.status_bar:
        config.status_bar.set_tool(name)


def activate_delete() -> None:
    _reset_tool_cid()
    config.cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_delete_click
    )
    _set_tool("Delete")
    plt.draw()


def activate_draw_point() -> None:
    _reset_tool_cid()
    config.cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_point
    )
    _set_tool("Point")
    plt.draw()


def activate_draw_line() -> None:
    _reset_tool_cid()
    config.cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_line
    )
    _set_tool("Line")
    plt.draw()


def activate_draw_segment() -> None:
    _reset_tool_cid()
    config.cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_segment
    )
    _set_tool("Segment")
    plt.draw()


def activate_draw_circle() -> None:
    _reset_tool_cid()
    config.circle_cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_circle
    )
    _set_tool("Circle")
    plt.draw()


def activate_draw_polygon() -> None:
    _reset_tool_cid()
    config.cid = config.ax.figure.canvas.mpl_connect(
        "button_press_event", _handle_polygon
    )
    _set_tool("Polygon")
    plt.draw()


# ── persistent canvas events ──────────────────────────────────────────────────

def on_key(event) -> None:
    if event.key in ("ctrl+z", "ctrl+Z"):
        from app.commands.history import undo
        undo()
    elif event.key in ("ctrl+y", "ctrl+Y"):
        from app.commands.history import redo
        redo()
    elif event.key == "delete" and config.last_shape:
        from app.commands.operations import delete_by_label
        delete_by_label(config.last_shape.get_label())


def on_press(event) -> None:
    if event.button == 1:
        config.selected_shape = _shape_at(event.xdata, event.ydata)

        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata

            if config.last_shape not in config.shapes:
                config.last_shape = None

            if config.last_shape is not None:
                w = find_widget_by_shape(config.last_shape)
                if w:
                    w.configure(fg=styles.TEXT)
                update_display()

            config.selected_shape.set_color("cyan")
            w = find_widget_by_shape(config.selected_shape)
            if w:
                w.configure(fg=styles.ACCENT_CYAN)
            config.last_widget = w
            config.last_shape  = config.selected_shape
            plt.draw()
        else:
            if config.last_shape is not None:
                w = find_widget_by_shape(config.last_shape)
                if w:
                    w.configure(fg=styles.TEXT)
                update_display()

    elif event.button == 3:
        shape = _shape_at(event.xdata, event.ydata)
        if isinstance(shape, Point) and config.set_shape == 0:
            config.selected_shape = shape
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata
            from app.ui.dialogs import open_insert_window
            open_insert_window(shape)


def on_release(event) -> None:
    if config.selected_shape is not None:
        config.selected_shape = None
        config.start_drag_x   = None
        config.start_drag_y   = None


def on_motion(event) -> None:
    if config.status_bar and event.xdata is not None and event.ydata is not None:
        config.status_bar.set_coords(event.xdata, event.ydata)

    if (config.selected_shape is None
            or event.xdata is None
            or event.ydata is None
            or event.button != 1):
        return

    dx = event.xdata - config.start_drag_x
    dy = event.ydata - config.start_drag_y
    config.start_drag_x, config.start_drag_y = event.xdata, event.ydata

    shape = config.selected_shape
    if isinstance(shape, Point):
        shape.set_x(dx)
        shape.set_y(dy)
    elif isinstance(shape, Circle):
        shape.get_center().set_x(dx)
        shape.get_center().set_y(dy)
    elif isinstance(shape, (Line, Segment)):
        shape.set_start_point(dx, dy)
        shape.set_end_point(dx, dy)

    update_display()
    update_label()
    plt.draw()


def on_axes_leave(event) -> None:
    if config.status_bar:
        config.status_bar.clear_coords()


def on_scroll(event) -> None:
    ax = config.ax
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    xl, xr = ax.get_xlim()
    yl, yr = ax.get_ylim()

    if event.button == "up":
        if xr - xl < 10 or yr - yl < 10:
            return
        factor = 0.95
    elif event.button == "down":
        xspan, yspan = xr - xl, yr - yl
        if xspan > 100 or yspan > 100 or xspan < 1 or yspan < 1:
            return
        factor = 1.05
    else:
        return

    ax.set_xlim(x - factor * (x - xl), x + factor * (xr - x))
    ax.set_ylim(y - factor * (y - yl), y + factor * (yr - y))
    ax.xaxis.set_ticks(range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 1))
    ax.yaxis.set_ticks(range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]) + 1))
    ax.grid(True, color=styles.CANVAS_GRID, linewidth=0.5)
    config.fig.canvas.draw_idle()


# ── shape-at-point detection ──────────────────────────────────────────────────

def _shape_at(x, y, threshold: float = 0.5):
    if x is None or y is None:
        return None
    for shape in config.shapes:
        if isinstance(shape, Point):
            try:
                if abs(x - shape.get_x()) <= threshold and abs(y - shape.get_y()) <= threshold:
                    return shape
            except TypeError:
                pass
        elif isinstance(shape, Circle):
            c    = shape.get_center()
            dist = np.sqrt((x - c.get_x()) ** 2 + (y - c.get_y()) ** 2)
            if abs(dist - shape.radius) <= threshold:
                return shape
        elif isinstance(shape, (Line, Segment)):
            m, b = shape.m_b()
            ly   = b if m is None else (m if b is None else m * x + b)
            if abs(y - ly) <= threshold:
                return shape
    return None


# ── drawing tool handlers ─────────────────────────────────────────────────────

def _handle_delete_click(event) -> None:
    if event.button == 1:
        shape = _shape_at(event.xdata, event.ydata)
        if shape is not None:
            from app.commands.operations import delete_by_label
            delete_by_label(shape.get_label())
    config.ax.figure.canvas.mpl_disconnect(config.cid)
    config.cid = None
    _set_tool("")


def _handle_point(event) -> None:
    if event.button != 1 or event.xdata is None:
        return
    from app.commands.operations import draw_shape
    draw_shape(Point(event.xdata, event.ydata, next(config.label_generator)))
    config.ax.figure.canvas.mpl_disconnect(config.cid)
    config.cid = None
    _set_tool("")


def _handle_line(event) -> None:
    if event.button != 1 or event.xdata is None:
        return
    from app.commands.operations import draw_shape

    if not config.line_x:
        config.line_x, config.line_y = event.xdata, event.ydata
        clicked = _shape_at(event.xdata, event.ydata)
        config.this_point = clicked if isinstance(clicked, Point) else None
        if config.status_bar:
            config.status_bar.set_tool("Line · click end")
        plt.draw()
        return

    if config.this_point:
        p1 = config.this_point
    else:
        p1 = Point(config.line_x, config.line_y, next(config.label_generator))
        draw_shape(p1)
        config.undo_stack.pop()

    p2   = Point(event.xdata, event.ydata, next(config.label_generator))
    line = Line(p1, p2, next(config.label_generator))
    draw_shape(p2);   config.undo_stack.pop()
    draw_shape(line)

    config.ax.figure.canvas.mpl_disconnect(config.cid)
    config.line_x = config.line_y = config.this_point = config.cid = None
    _set_tool("")
    plt.draw()


def _handle_segment(event) -> None:
    if event.button != 1 or event.xdata is None:
        return
    from app.commands.operations import draw_shape

    if not config.segment_x:
        config.segment_x, config.segment_y = event.xdata, event.ydata
        clicked = _shape_at(event.xdata, event.ydata)
        config.this_point = clicked if isinstance(clicked, Point) else None
        if config.status_bar:
            config.status_bar.set_tool("Segment · click end")
        plt.draw()
        return

    if config.this_point:
        p1 = config.this_point
    else:
        p1 = Point(config.segment_x, config.segment_y, next(config.label_generator))
        draw_shape(p1)
        config.undo_stack.pop()

    p2      = Point(event.xdata, event.ydata, next(config.label_generator))
    segment = Segment(p1, p2, next(config.label_generator))
    draw_shape(p2);      config.undo_stack.pop()
    draw_shape(segment)

    config.ax.figure.canvas.mpl_disconnect(config.cid)
    config.segment_x = config.segment_y = config.this_point = config.cid = None
    _set_tool("")
    plt.draw()


def _handle_circle(event) -> None:
    if event.button != 1 or event.xdata is None:
        return
    from app.commands.operations import draw_shape

    if not config.circle_x:
        config.circle_x, config.circle_y = event.xdata, event.ydata
        clicked = _shape_at(event.xdata, event.ydata)
        config.this_point = clicked if isinstance(clicked, Point) else None
        if config.status_bar:
            config.status_bar.set_tool("Circle · click radius")
        plt.draw()
        return

    x, y = event.xdata, event.ydata
    if config.this_point:
        cx, cy = config.this_point.get_x(), config.this_point.get_y()
        center = config.this_point
    else:
        cx, cy = config.circle_x, config.circle_y
        center = Point(cx, cy, next(config.label_generator))
        draw_shape(center)
        config.undo_stack.pop()

    radius = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    circle = Circle(center, radius, next(config.label_generator))
    draw_shape(circle)

    config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
    config.circle_cid = config.circle_x = config.circle_y = config.this_point = None
    _set_tool("")


def _handle_polygon(event) -> None:
    if event.button != 1 or event.xdata is None:
        return
    from app.commands.operations import draw_shape

    if not config.curr_polygon:
        config.curr_polygon = Polygon([], "")
        config.polygon_x, config.polygon_y = event.xdata, event.ydata
        fp = Point(event.xdata, event.ydata, next(config.label_generator))
        config.first_point_polygon = fp
        config.curr_polygon.set_label(fp.get_label())
        config.last_point_polygon = fp
        if config.status_bar:
            config.status_bar.set_tool("Polygon · adding vertices")
        plt.draw()
        return

    if _shape_at(event.xdata, event.ydata) is config.first_point_polygon:
        p1  = config.last_point_polygon
        p2  = config.first_point_polygon
        seg = Segment(p1, p2, next(config.label_generator))
        config.curr_polygon.add_segment(seg)

        draw_shape(p1);  config.shapes.pop();  config.undo_stack.pop()
        draw_shape(p2);  config.shapes.pop();  config.undo_stack.pop()
        draw_shape(seg);                        config.undo_stack.pop()

        config.curr_polygon.set_label(p2.get_label())
        config.shapes.append(config.curr_polygon)
        config.undo_stack.append({"type": "draw", "shape": config.curr_polygon})

        config.ax.figure.canvas.mpl_disconnect(config.cid)
        config.first_point_polygon = config.last_point_polygon = None
        config.curr_polygon = config.polygon_x = config.polygon_y = config.cid = None

        from app.ui.algo_panel import refresh_shape_dropdown
        refresh_shape_dropdown()
        _set_tool("")
        plt.draw()
        return

    p1  = config.last_point_polygon
    p2  = Point(event.xdata, event.ydata, next(config.label_generator))
    seg = Segment(p1, p2, next(config.label_generator))

    config.curr_polygon.set_label(p2.get_label())
    config.curr_polygon.add_segment(seg)

    draw_shape(p1)
    if config.first_point_polygon is not config.last_point_polygon:
        config.shapes.pop()
    draw_shape(p2);  config.undo_stack.pop()
    draw_shape(seg); config.undo_stack.pop()
    config.undo_stack.pop()

    config.last_point_polygon = p2
    plt.draw()
