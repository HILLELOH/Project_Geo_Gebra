import json
from pprint import pprint
from tkinter import ttk, filedialog

import numpy as np
import tkinter as tk

from PIL import ImageTk
from matplotlib import pyplot as plt

from Shapes.Circle import *
from Shapes.Point import *
from Shapes.Line import *
# from config import root, fig, ax
import config


class SidePanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)


def init_program():
    config.root.geometry("1400x900")
    config.root.resizable(False, False)
    config.root.wm_title("Geogebra")

    config.fig.set_size_inches(8, 8)
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')
    config.ax.grid(True)

    # Set the number of ticks and their intervals
    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))
    # center_spines()
    # Add horizontal and vertical lines to show the origin
    config.ax.axhline(0, color='black', linewidth=0.5)
    config.ax.axvline(0, color='black', linewidth=0.5)
    config.buttons_panel.pack(side=tk.TOP, fill=tk.X)


global button_list, file_button


def create_buttons():
    global button_list, file_button
    point_button = tk.Button(config.buttons_panel, text="Draw Point", command=draw_point)
    line_button = tk.Button(config.buttons_panel, text="Draw Line", command=draw_line)
    circle_button = tk.Button(config.buttons_panel, text="Draw Circle", command=draw_circle)
    # polygon_button = tk.Button(config.buttons_panel, text="polygon", command=draw_polygon)
    reset_button = tk.Button(config.buttons_panel, text="Reset", command=reset)
    save_button = tk.Button(config.buttons_panel, text="Save", command=save)
    load_button = tk.Button(config.buttons_panel, text="Load file", command=load)
    delete_button = tk.Button(config.buttons_panel, text="Delete shape", command=delete_shape)
    undo_button = tk.Button(config.buttons_panel, text="undo", command=undo)
    redo_button = tk.Button(config.buttons_panel, text="redo", command=redo)
    clear_history_button = tk.Button(config.buttons_panel, text="clear history", command=clear_history)

    buttons = [save_button,
               load_button,
               delete_button,
               reset_button,

               point_button,
               line_button,
               circle_button,
               # polygon_button,

               # file_button,
               clear_history_button,
               redo_button,
               undo_button]

    padding = 2
    right = [clear_history_button,
             undo_button,
             redo_button, ]
    for i in range(len(buttons)):
        if buttons[i] in right:
            buttons[i].pack(side=tk.RIGHT, padx=padding)
        # buttons[i].pack(side=tk.RIGHT, padx=padding)
        else:
            buttons[i].pack(side=tk.LEFT, padx=padding)

    # make_file_button_frame(config.file_frame)


def is_start_end(p, line):
    threshold = 0.05

    if abs(p.get_x() - line.get_start_point()[0]) < threshold and abs(
            p.get_y() - line.get_start_point()[1]) < threshold:
        return "start"

    elif abs(p.get_x() - line.get_end_point()[0]) < threshold and abs(p.get_y() - line.get_end_point()[1]) < threshold:
        return "end"

    else:
        # return f'{abs(coords[0] - line.get_start_point()[0])}, {abs(coords[1] - line.get_start_point()[1])}\n' \
        #        f'{abs(coords[0] - line.get_end_point()[0])}, {abs(coords[1] - line.get_end_point()[1])}'
        return None


def shape_clicked(x, y):
    threshold = 0.5
    for shape in config.shapes:
        if isinstance(shape, Point):
            try:
                if np.abs(x - shape.get_x()) <= threshold and np.abs(y - shape.get_y()) <= threshold:
                    return shape
            except TypeError:
                print("")

        elif isinstance(shape, Circle):
            circle_x = shape.coords[0][0]
            circle_y = shape.coords[0][0]
            distance = np.sqrt((x - circle_x) ** 2 + (y - circle_y) ** 2)
            if np.abs(distance - shape.radius) <= threshold:
                return shape

        # elif isinstance(shape, Line):
        #     m, b = shape.m_b()
        #     line_y = m * x + b
        #     if np.abs(y - line_y) <= threshold:
        #         return shape
    return None


def on_press(event):
    if event.button == 1:  # Left mouse button
        config.selected_shape = shape_clicked(event.xdata, event.ydata)
        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata


def on_release(event):
    if config.selected_shape is not None:
        config.selected_shape = None
        config.start_drag_x, config.start_drag_y = None, None


def on_motion(event):
    if config.selected_shape is not None and event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        dx = x - config.start_drag_x
        dy = y - config.start_drag_y
        config.start_drag_x, config.start_drag_y = x, y

        # if isinstance(config.selected_shape, Line):  # Check if the selected_shape is a Line
        #     m, b = config.selected_shape.m_b()
        #     b += dy  # Update the y-intercept of the line
        #     xdata, ydata = config.selected_shape.line_obj.get_data()
        #     ydata = m * xdata + b
        #     config.selected_shape.line_obj.set_data(xdata, ydata)

        if isinstance(config.selected_shape, Point):
            flag = False
            for shape in config.shapes:
                if isinstance(shape, Line):
                    if shape.is_line_edge(config.selected_shape)[1] == "start":
                        print("start")
                        print(config.selected_shape)
                        config.selected_shape.coords[0][0] += dx
                        config.selected_shape.coords[0][1] += dy
                        config.selected_shape.set_x(dx)
                        config.selected_shape.set_y(dy)

                        shape.set_start_point(dx, dy)
                        flag = True
                        break

                    elif shape.is_line_edge(config.selected_shape)[1] == "end":
                        print("end")
                        config.selected_shape.coords[0][0] += dx
                        config.selected_shape.coords[0][1] += dy
                        config.selected_shape.set_x(dx)
                        config.selected_shape.set_y(dy)
                        shape.set_end_point(dx, dy)
                        flag = True
                        break

            if not flag:
                config.selected_shape.coords[0][0] += dx
                config.selected_shape.coords[0][1] += dy
                config.selected_shape.set_x(dx)
                config.selected_shape.set_y(dy)


        elif isinstance(config.selected_shape, Circle):
            config.selected_shape.coords[0][0] += dx
            config.selected_shape.coords[0][1] += dy

        update_display()
        update_label()
        plt.draw()


def delete_shape():
    if not config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if not config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_delete_shape)
    plt.title("Click shape to delete")
    plt.draw()


def draw_point():
    if not config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if not config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_point)
    plt.title("Click left mouse button to create point")
    plt.draw()


def draw_line():
    if config.cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if config.circle_cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_line)
    plt.title("Click left mouse button to start line")
    plt.draw()


def draw_circle():
    if config.cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if config.circle_cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_circle)
    plt.title("Click left mouse button to set center")
    plt.draw()


# def draw_polygon():
#     if config.cid is not None:
#         config.ax.figure.canvas.mpl_disconnect(config.cid)
#
#     if config.circle_cid is not None:
#         config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
#
#     config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_polygon)
#     plt.title("Click left mouse button to set points")
#     plt.draw()


def handle_input_circle(event):
    if event.button == 1:  # Left mouse button
        if not config.circle_x and not config.circle_x:  # first click
            config.circle_x, config.circle_y = event.xdata, event.ydata
            config.ax.set_title("Click left click again to set the radius")
            config.ax.figure.canvas.draw()

        else:  # second click
            x, y = event.xdata, event.ydata
            radius = np.sqrt((x - config.circle_x) ** 2 + (y - config.circle_y) ** 2)
            draw_circle_shape(config.circle_x, config.circle_y, radius)

            # Disconnect the circle event listener so it doesn't interfere with other shapes
            config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
            config.circle_cid, config.circle_x, config.circle_y = [None] * 3


def handle_input_point(event):
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        draw_point_shape(x, y)

        # Disconnect the event listener so points can't be drawn anymore
        config.ax.figure.canvas.mpl_disconnect(config.cid)


def handle_input_line(event):
    if event.button == 1:  # Left mouse button
        if not config.line_x and not config.line_y:
            # First click sets the start point
            config.line_x, config.line_y = event.xdata, event.ydata
            plt.title("Click left click to draw the end point")
            plt.draw()

        else:
            # Second click sets the end point
            p1 = Point((config.line_x, config.line_y))
            p2 = Point((event.xdata, event.ydata))
            line = Line(p1, p2)
            draw_line_shape(line)

            config.ax.figure.canvas.mpl_disconnect(config.cid)
            # Remove start_point attribute so user can draw another line
            config.line_x, config.line_y = [None] * 2
            plt.title("")
            plt.draw()


#
# def handle_input_polygon(event):
#     if event.button == 1:  # Left mouse button
#         if len(config.polygon_vertices) == 0:
#             draw_point_shape(event.xdata, event.ydata)
#             config.polygon_vertices.append((event.xdata, event.ydata))
#         else:
#             if (event.xdata, event.ydata) == (config.polygon_vertices[0]):
#                 draw_point_shape(event.xdata, event.ydata)
#                 last_point = config.polygon_vertices[-1]
#                 line = Line((event.xdata, event.ydata), (last_point[0], last_point[1]))
#                 draw_line_shape(line)
#                 config.polygon_vertices.append((event.xdata, event.ydata))
#
#                 config.ax.figure.canvas.mpl_disconnect(config.cid)
#                 # Remove start_point attribute so user can draw another line
#                 config.polygon_vertices = []
#                 plt.title("")
#                 plt.draw()
#
#             else:
#                 draw_point_shape(event.xdata, event.ydata)
#                 last_point = config.polygon_vertices[-1]
#                 p1 = Point((event.xdata, event.ydata))
#                 p2 = Point((last_point[0], last_point[1]))
#                 line = Line(p1, p2)
#                 draw_line_shape(line)
#                 config.polygon_vertices.append((event.xdata, event.ydata))
#
#                 config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_polygon)


def handle_delete_shape(event):
    if event.button == 1:
        shape = shape_clicked(event.xdata, event.ydata)
        if shape is not None:
            # if isinstance(shape, Line):
            #     start = Point((shape.x1, shape.y1))
            #     end = Point((shape.x2, shape.y2))
            #     command = {"type": 'delete', "shape": shape, "start": start, "end": end}
            #     config.undo_stack.insert(len(config.undo_stack), command)
            #
            #     config.shapes.remove(start)
            #     config.shapes.remove(end)
            #     config.shapes.remove(shape)

            if isinstance(shape, Point):
                flag = False
                for s in config.shapes:
                    if isinstance(s, Line):
                        print(s.is_line_edge(shape)[0])
                        if s.is_line_edge(shape)[0] is True:
                            command = {"type": 'delete', "shape": s, "start": s.get_start(), "end": s.get_end()}
                            config.undo_stack.insert(len(config.undo_stack), command)

                            print(s.get_start_point())
                            # for s in config.shapes:
                            #     if isinstance(s, Line):
                            #         print(type(s.get_start_point()))
                            config.shapes.remove(s.get_start())
                            config.shapes.remove(s.get_end())
                            config.shapes.remove(s)
                            flag = True
                            break

                if not flag:
                    print("askdpasd")
                    command = {"type": 'delete', "shape": shape}
                    config.undo_stack.insert(len(config.undo_stack), command)
                    config.shapes.remove(shape)

            else:
                command = {"type": 'delete', "shape": shape}
                config.undo_stack.insert(len(config.undo_stack), command)
                config.shapes.remove(shape)

            update_display()
            update_label()


def draw_point_shape(x, y):
    point = Point((x, y))
    point.draw(config.ax)
    config.shapes.append(point)

    command = {"type": 'draw', "shape": config.shapes[-1], "coords": (config.circle_x, config.circle_y)}
    config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def draw_line_shape(line):
    start = line.get_start()
    end = line.get_end()

    start.draw(config.ax)
    end.draw(config.ax)

    config.shapes.append(start)
    config.shapes.append(end)

    line.draw(config.ax)
    config.shapes.append(line)

    command = {"type": 'draw', "shape": config.shapes[-1], "start": start, "end": end}
    config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def draw_circle_shape(x, y, radius):
    circle = Circle([(x, y)], radius)
    circle.draw(config.ax)
    config.shapes.append(circle)

    command = {"type": 'draw', "shape": config.shapes[-1], "coords": (config.circle_x, config.circle_y),
               "radius": radius}
    config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def run():
    plt.show()


def update_display():
    config.ax.cla()
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')  # Set the aspect ratio to 'equal'
    config.ax.grid(True)
    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))

    for shape in config.shapes:
        shape.draw(config.ax)

    plt.draw()


def update_label():
    global label_text, coords
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []

    for shape in config.shapes:

        if isinstance(shape, Line):
            m, b = shape.m_b()
            label_text = f'Line: y = {m:.3f}x + {b:.3f}'

        elif isinstance(shape, Point):
            try:
                label_text = f'Point: ({shape.get_x():.3f}, {shape.get_y():.3f})'

            except TypeError:
                print(f'coords: {coords}')

        elif isinstance(shape, Circle):
            x, y = shape.coords[0]
            r = shape.radius
            label_text = f'Circle: (x-{x:.3f})^2 + (y-{y:.3f})^2 = {r ** 2:.3f}'

        label_widget = tk.Label(config.side_panel.text, text=label_text, bg='white')
        label_widget.pack(anchor='w')
        config.label_widgets.append(label_widget)


def reset():
    config.ax.clear()
    config.shapes = []
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []

    # Reset the axes and grid
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')
    config.ax.grid(True)
    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))

    plt.draw()


def save():
    global shape_data
    filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not filepath:
        return
    shapes_data = []
    for shape in config.shapes:

        shape_type = type(shape).__name__
        if isinstance(shape, Line):
            shape_data = {"p1": [shape.x1, shape.y1], "p2": [shape.x2, shape.y2]}

        elif isinstance(shape, Circle):
            shape_coords = shape.coords.tolist()
            print(f'her: {shape_coords}')
            shape_data = {"coords": shape_coords[0], "radius": shape.radius}

        elif isinstance(shape, Point):
            shape_coords = shape.coords.tolist()
            shape_data = {
                "coords": shape_coords[0][0],
            }

        shapes_data.append(shape_data)

    print(shapes_data)
    with open(filepath, 'w') as f:
        json.dump(shapes_data, f)


def load():
    filename = filedialog.askopenfilename()
    # print(filename)
    if not filename or not filename.endswith(".json"):
        return
    with open(filename, 'r') as f:
        print(filename)
        shapes_data = json.load(f)
    reset()

    for shape in shapes_data:
        if isinstance(shape, Line):
            p1 = shape_data["p1"]
            p2 = shape_data["p2"]
            line = Line(p1, p2)
            draw_line_shape(line)
            draw_point_shape(p1[0], p1[1])
            draw_point_shape(p2[0], p2[1])

        elif isinstance(shape, Circle):
            coords = shape_data["coords"]
            radius = shape_data["radius"]
            draw_circle_shape(coords[0], coords[1], radius)

        elif isinstance(shape, Point):
            coords = shape_data["coords"]
            print(coords)
            draw_point_shape(coords[0], coords[1])


# def load():
#     filename = filedialog.askopenfilename()
#     # print(filename)
#     if not filename or not filename.endswith(".json"):
#         return
#     with open(filename, 'r') as f:
#         print(filename)
#         shapes_data = json.load(f)
#     reset()
#
#     print(shapes_data)
#     for shape_data in shapes_data:
#         shape_type = shape_data["type"]
#
#         if shape_type == "Point":
#             coords = shape_data["coords"]
#             print(len(coords))
#             draw_point_shape(coords[0], coords[1])
#
#         elif shape_type == "Line":
#             p1 = shape_data["p1"]
#             p2 = shape_data["p2"]
#             line = Line(p1, p2)
#             draw_line_shape(line)
#
#         elif shape_type == "Circle":
#             coords = shape_data["coords"]
#             radius = shape_data["radius"]
#             draw_circle_shape(coords[0], coords[1], radius)


def do_same_command(command):
    config.last_command = command
    if command["type"] == 'delete':
        shape = command["shape"]
        if isinstance(shape, Point):
            config.shapes.remove(shape)

        if isinstance(shape, Line):
            # pprint(config.shapes)

            config.shapes.remove(command["start"])
            config.shapes.remove(command["end"])
            config.shapes.remove(shape)
            # pprint(config.shapes)

        update_display()
        update_label()

    elif command["type"] == 'draw':
        shape = command["shape"]

        if isinstance(shape, Line):
            p1 = shape.get_start()
            p2 = shape.get_end()
            line = Line(p1, p2)
            draw_line_shape(line)

        elif isinstance(shape, Point):
            coords = shape.coords.tolist()[0][0]
            draw_point_shape(coords[0], coords[1])

        elif isinstance(shape, Circle):
            coords = shape.coords.tolist()[0]
            draw_circle_shape(coords[0], coords[1], shape.radius)

    # elif command["type"] is 'move':


def do_opposite_command(command):
    config.last_command = command
    if command["type"] == 'draw':
        shape = command["shape"]
        if isinstance(shape, Line):
            to_del = []
            for s in config.shapes:
                if isinstance(s, Point):
                    if is_start_end(s, shape) is not None:
                        to_del.append(s)
            [config.shapes.remove(s) for s in to_del]

        config.shapes.remove(shape)
        update_display()
        update_label()

    elif command["type"] == 'delete':
        shape = command["shape"]

        if isinstance(shape, Line):
            p1 = shape.get_start()
            p2 = shape.get_end()
            line = Line(p1, p2)
            draw_line_shape(line)

        elif isinstance(shape, Point):
            coords = shape.coords.tolist()[0][0]
            draw_point_shape(coords[0], coords[1])

        elif isinstance(shape, Circle):
            coords = shape.coords.tolist()[0]
            draw_circle_shape(coords[0], coords[1], shape.radius)


def redo():
    try:
        if config.redo_stack is not None:
            command = config.redo_stack.pop()
            do_same_command(command)
            config.undo_stack.insert(len(config.redo_stack), command)
    except IndexError:
        print("")


def undo():
    try:
        if config.undo_stack is not None:
            command = config.undo_stack.pop()
            pprint(config.shapes)
            do_opposite_command(command)
            pprint(config.shapes)
            config.redo_stack.insert(len(config.redo_stack), command)
    except IndexError:
        print("")


def clear_history():
    config.undo_stack = []
    config.redo_stack = []
