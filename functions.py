import json
from tkinter import ttk, filedialog

import numpy as np
import tkinter as tk
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


def create_buttons():
    point_button = tk.Button(config.root, text="Draw Point", command=draw_point)
    line_button = tk.Button(config.root, text="Draw Line", command=draw_line)
    circle_button = tk.Button(config.root, text="Draw Circle", command=draw_circle)
    reset_button = tk.Button(config.root, text="Reset", command=reset)
    save_button = tk.Button(config.root, text="Save state", command=save)
    load_button = tk.Button(config.root, text="Load file", command=load)

    buttons = [point_button,
               line_button,
               circle_button,
               reset_button,
               save_button,
               load_button]

    padding = 5
    for i in range(len(buttons)):
        buttons[i].pack(padx=padding)
        padding += buttons[i].winfo_width()


def shape_clicked(x, y):
    threshold = 0.5
    for shape in config.shapes:
        if isinstance(shape, Point):
            point_x, point_y = shape.coords[0][0]
            if np.abs(x - point_x) <= threshold and np.abs(y - point_y) <= threshold:
                return shape

        elif isinstance(shape, Circle):
            circle_x, circle_y = shape.coords[0]
            distance = np.sqrt((x - circle_x) ** 2 + (y - circle_y) ** 2)
            if np.abs(distance - shape.radius) <= threshold:
                return shape

        elif isinstance(shape, Line):  # Add this block to handle lines
            line_y = shape.m * x + shape.b
            if np.abs(y - line_y) <= threshold:
                return shape
    return None


def on_press(event):
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        config.selected_shape = shape_clicked(x, y)
        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = x, y


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

        if isinstance(config.selected_shape, Point):
            config.selected_shape.coords[0][0][0] += dx
            config.selected_shape.coords[0][0][1] += dy

        elif isinstance(config.selected_shape, Circle):
            config.selected_shape.coords[0][0] += dx
            config.selected_shape.coords[0][1] += dy

        elif isinstance(config.selected_shape, Line):  # Check if the selected_shape is a Line
            config.selected_shape.b += dy  # Update the y-intercept of the line
            xdata, ydata = config.selected_shape.line_obj.get_data()
            ydata = config.selected_shape.m * xdata + config.selected_shape.b
            config.selected_shape.line_obj.set_data(xdata, ydata)

        update_display()
        update_label()
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


# def handle_input_circle(event):
#     if event.button == 1:  # Left mouse button
#         if event.xdata is not None and event.ydata is not None:
#             x1, y1 = event.xdata, event.ydata
#             plt.title("Click left click to set the radius")
#             plt.draw()
#             points = plt.ginput(1, timeout=-1, mouse_add=1)  # Wait for left click
#             if points:
#                 x2, y2 = points[0]
#                 radius = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#                 draw_circle_shape(x1, y1, radius)
#                 # Disconnect the circle event listener so it doesn't interfere with other shapes
#                 config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
#                 config.circle_cid = None  # Reset the circle event listener variable to None

# def handle_input_circle(event):
#     if event.button == 1:  # Left mouse button
#         if not event.xdata and not event.ydata:
#             x1, y1 = event.xdata, event.ydata
#             plt.title("Click left click to set the radius")
#             plt.draw()
#             points = plt.ginput(1, timeout=-1)
#             if points:
#                 x2, y2 = points[0]
#                 radius = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#                 draw_circle_shape(x1, y1, radius)
#                 # Disconnect the circle event listener so it doesn't interfere with other shapes
#                 config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
#                 config.circle_cid = None  # Reset the circle event listener variable to None

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
            config.circle_cid = None
            config.circle_x, config.circle_y = [None]*2


def handle_input_point(event):
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        draw_point_shape(x, y)
        # Disconnect the event listener so points can't be drawn anymore
        config.ax.figure.canvas.mpl_disconnect(config.cid)


# def handle_input_line(event):
#     if event.button == 1:  # Left mouse button
#         if not hasattr('start_point'):
#             # First click sets the start point
#             config.start_point = (event.xdata, event.ydata)
#             plt.title("Click left click to draw the end point")
#             plt.draw()
#         else:
#             # Second click sets the end point
#             end_point = (event.xdata, event.ydata)
#             m, b = m_b(config.start_point[0], config.start_point[1], end_point[0], end_point[1])
#             draw_line_shape(m, b)
#             # Remove start_point attribute so user can draw another line
#             delattr('start_point')
#             plt.title("")
#             plt.draw()

def handle_input_line(event):
    if event.button == 1:  # Left mouse button
        if not config.line_x and not config.line_y:
            # First click sets the start point
            config.line_x, config.line_y = event.xdata, event.ydata
            plt.title("Click left click to draw the end point")
            plt.draw()

        else:
            # Second click sets the end point
            end_point = (event.xdata, event.ydata)
            m, b = m_b(config.line_x, config.line_y, end_point[0], end_point[1])
            draw_line_shape(m, b)
            config.ax.figure.canvas.mpl_disconnect(config.cid)
            # Remove start_point attribute so user can draw another line
            config.line_x, config.line_y = [None]*2
            plt.title("")
            plt.draw()


def draw_point_shape(x, y):
    point = Point([(x, y)])
    point.draw(config.ax)
    config.shapes.append(point)
    update_display()
    update_label()


def m_b(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b


def draw_line_shape(m, b):
    x = np.linspace(-10, 10, 100)
    y = m * x + b
    line = Line(m, b)

    line.draw(config.ax)

    config.shapes.append(line)
    update_display()
    update_label()


def draw_circle_shape(x, y, radius):
    circle = Circle([(x, y)], radius)
    circle.draw(config.ax)
    config.shapes.append(circle)
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

    for shape in config.shapes:
        shape.draw(config.ax)

    plt.draw()


def update_label():
    global label_text
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []

    for shape in config.shapes:
        if isinstance(shape, Point):
            label_text = f'Point: ({shape.coords[0][0][0]:.1f}, {shape.coords[0][0][1]:.1f})'

        elif isinstance(shape, Circle):
            x, y = shape.coords[0]
            r = shape.radius
            label_text = f'Circle: (x-{x:.1f})^2 + (y-{y:.1f})^2 = {r**2:.1f}'

        elif isinstance(shape, Line):
            label_text = f'Line: y = {shape.m:.1f}x + {shape.b:.1f}'

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
            shape_data = {"type": shape_type, "m": shape.m, "b": shape.b}

        elif isinstance(shape, Circle):
            shape_coords = shape.coords.tolist()
            shape_data = {"type": shape_type, "coords": shape_coords[0], "radius": shape.radius}

        elif isinstance(shape, Point):
            shape_coords = shape.coords.tolist()
            shape_data = {
                "type": shape_type,
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

    print(shapes_data)
    for shape_data in shapes_data:
        shape_type = shape_data["type"]

        if shape_type == "Point":
            coords = shape_data["coords"]
            print(len(coords))
            draw_point_shape(coords[0], coords[1])

        elif shape_type == "Line":
            m = shape_data["m"]
            b = shape_data["b"]
            draw_line_shape(m, b)

        elif shape_type == "Circle":
            coords = shape_data["coords"]
            radius = shape_data["radius"]
            draw_circle_shape(coords[0], coords[1], radius)












