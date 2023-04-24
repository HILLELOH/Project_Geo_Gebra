import json
import os

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from tkinter import ttk, filedialog, simpledialog

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm

# refactor
from Shapes.Circle import *
from Shapes.Point import *
from Shapes.Line import *



class SidePanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1400x900")
        self.root.resizable(False, False)
        self.root.wm_title("Geogebra-like Tool")

        # Create the squared XY plane
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 8)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')
        ax.grid(True)

        # Set the number of ticks and their intervals
        ax.set_xticks(np.arange(-20, 21, 5))
        ax.set_yticks(np.arange(-20, 21, 5))
        # center_spines()
        # Add horizontal and vertical lines to show the origin
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        self.ax = ax
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)

        #self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

        # Empty list of shapes
        self.shapes = []
        self.label_widgets = []

        # Create buttons for drawing points, lines, and circles
        self.point_button = tk.Button(self.root, text="Draw Point", command=self.draw_point)
        self.line_button = tk.Button(self.root, text="Draw Line", command=self.draw_line)
        self.circle_button = tk.Button(self.root, text="Draw Circle", command=self.draw_circle)
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.save_button = tk.Button(self.root, text="Save state", command=self.save)
        self.load_button = tk.Button(self.root, text="Load file", command=self.load)

        buttons = [self.point_button,
                   self.line_button,
                   self.circle_button,
                   self.reset_button,
                   self.save_button,
                   self.load_button]
        self.align_buttons(buttons)

        self.side_panel = SidePanel(self.root)
        self.side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cid = None
        self.circle_cid = None
        self.press_cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.release_cid = self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.motion_cid = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.selected_shape, self.start_drag_x, self.start_drag_y = [None] * 3

        self.update_display()

    def align_buttons(self, buttons):
        padding = 5
        for i in range(len(buttons)):
            buttons[i].pack(padx=padding)
            padding += buttons[i].winfo_width()

    def reset(self):
        self.ax.clear()
        self.shapes = []
        for widget in self.label_widgets:
            widget.destroy()
        self.label_widgets = []

        # Reset the axes and grid
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_xticks(np.arange(-20, 21, 5))
        self.ax.set_yticks(np.arange(-20, 21, 5))

        plt.draw()

    def save(self):
        global shape_data
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return
        shapes_data = []
        for shape in self.shapes:
            shape_type = type(shape).__name__
            if isinstance(shape, Line):
                shape_data = {
                    "type": shape_type,
                }
                shape_data["m"] = shape.m
                shape_data["b"] = shape.b

            elif isinstance(shape, Circle):
                shape_coords = shape.coords.tolist()
                shape_data = {
                    "type": shape_type,
                    "coords": shape_coords[0],
                }
                shape_data["radius"] = shape.radius

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

    def load(self):
        global shape
        filename = filedialog.askopenfilename()
        # print(filename)
        if not filename or not filename.endswith(".json"):
            return
        with open(filename, 'r') as f:
            print(filename)
            shapes_data = json.load(f)
        self.reset()

        print(shapes_data)
        for shape_data in shapes_data:
            shape_type = shape_data["type"]

            if shape_type == "Point":
                coords = shape_data["coords"]
                print(len(coords))
                self.draw_point_shape(coords[0], coords[1])

            elif shape_type == "Line":
                m = shape_data["m"]
                b = shape_data["b"]
                self.draw_line_shape(m, b)

            elif shape_type == "Circle":
                coords = shape_data["coords"]
                radius = shape_data["radius"]
                self.draw_circle_shape(coords[0], coords[1], radius)

    def shape_clicked(self, x, y):
        threshold = 0.5
        for shape in self.shapes:
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

    def on_press(self, event):
        if event.button == 1:  # Left mouse button
            x, y = event.xdata, event.ydata
            self.selected_shape = self.shape_clicked(x, y)
            if self.selected_shape is not None:
                self.start_drag_x, self.start_drag_y = x, y

    def on_release(self, event):
        if self.selected_shape is not None:
            self.selected_shape = None
            self.start_drag_x, self.start_drag_y = None, None

    def on_motion(self, event):
        if self.selected_shape is not None and event.xdata is not None and event.ydata is not None:
            x, y = event.xdata, event.ydata
            dx = x - self.start_drag_x
            dy = y - self.start_drag_y
            self.start_drag_x, self.start_drag_y = x, y

            if isinstance(self.selected_shape, Point):
                self.selected_shape.coords[0][0][0] += dx
                self.selected_shape.coords[0][0][1] += dy

            elif isinstance(self.selected_shape, Circle):
                self.selected_shape.coords[0][0] += dx
                self.selected_shape.coords[0][1] += dy

            elif isinstance(self.selected_shape, Line):  # Check if the selected_shape is a Line
                self.selected_shape.b += dy  # Update the y-intercept of the line
                xdata, ydata = self.selected_shape.line_obj.get_data()
                ydata = self.selected_shape.m * xdata + self.selected_shape.b
                self.selected_shape.line_obj.set_data(xdata, ydata)

            self.update_display()
            self.update_label()
            plt.draw()


    def draw_point(self):
        if not self.cid:
            self.ax.figure.canvas.mpl_disconnect(self.cid)

        if not self.circle_cid:
            self.ax.figure.canvas.mpl_disconnect(self.circle_cid)

        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.handle_input_point)
        plt.title("Click left mouse button to create point")
        plt.draw()

    def draw_line(self):
        if self.cid is not None:
            self.ax.figure.canvas.mpl_disconnect(self.cid)

        if self.circle_cid is not None:
            self.ax.figure.canvas.mpl_disconnect(self.circle_cid)

        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.handle_input_line)
        plt.title("Click left mouse button to start line")
        plt.draw()

    def draw_circle(self):
        if self.cid is not None:
            self.ax.figure.canvas.mpl_disconnect(self.cid)

        if self.circle_cid is not None:
            self.ax.figure.canvas.mpl_disconnect(self.circle_cid)

        self.circle_cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.handle_input_circle)
        plt.title("Click left mouse button to set center")
        plt.draw()

    # def handle_input_circle(self, event):
    #     if event.button == 1:  # Left mouse button
    #         if not event.xdata and not event.ydata:
    #             if not hasattr(self, 'x1') or not hasattr(self, 'y1'):  # first click
    #                 self.x1, self.y1 = event.xdata, event.ydata
    #                 plt.title("Click left click again to set the radius")
    #                 plt.draw()
    #             else:  # second click
    #                 x2, y2 = event.xdata, event.ydata
    #                 radius = np.sqrt((x2 - self.x1) ** 2 + (y2 - self.y1) ** 2)
    #                 self.draw_circle_shape(self.x1, self.y1, radius)
    #                 # Disconnect the circle event listener so it doesn't interfere with other shapes
    #                 self.ax.figure.canvas.mpl_disconnect(self.circle_cid)
    #                 self.circle_cid = None  # Reset the circle event listener variable to None
    #                 # Reset x1 and y1 for the next circle
    #                 self.x1, self.y1 = None, None

    def handle_input_circle(self, event):
        if event.button == 2:  # Left mouse button
            if event.xdata is not None and event.ydata is not None:
                x1, y1 = event.xdata, event.ydata
                plt.title("Click left click to set the radius")
                plt.draw()
                points = plt.ginput(1, timeout=-1)
                if points:
                    x2, y2 = points[0]
                    radius = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    self.draw_circle_shape(x1, y1, radius)
                    # Disconnect the circle event listener so it doesn't interfere with other shapes
                    self.ax.figure.canvas.mpl_disconnect(self.circle_cid)
                    self.circle_cid = None  # Reset the circle event listener variable to None

    def handle_input_point(self, event):
        if event.button == 1:  # Left mouse button
            x, y = event.xdata, event.ydata
            self.draw_point_shape(x, y)
            # Disconnect the event listener so points can't be drawn anymore
            self.ax.figure.canvas.mpl_disconnect(self.cid)

    def handle_input_line(self, event):
        if event.button == 1:  # Left mouse button
            if not hasattr(self, 'start_point'):
                # First click sets the start point
                self.start_point = (event.xdata, event.ydata)
                plt.title("Click left click to draw the end point")
                plt.draw()
            else:
                # Second click sets the end point
                end_point = (event.xdata, event.ydata)
                m, b = self.m_b(self.start_point[0], self.start_point[1], end_point[0], end_point[1])
                self.draw_line_shape(m, b)
                # Remove start_point attribute so user can draw another line
                delattr(self, 'start_point')
                plt.title("")
                plt.draw()

    def draw_point_shape(self, x, y):
        point = Point([(x, y)])
        point.draw(self.ax)
        self.shapes.append(point)
        self.update_display()
        self.update_label()

    def m_b(self, x1, y1, x2, y2):
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return m, b

    def draw_line_shape(self, m, b):
        x = np.linspace(-10, 10, 100)
        y = m * x + b
        line = Line(m, b)

        line.draw(self.ax)

        self.shapes.append(line)
        self.update_display()
        self.update_label()

    def draw_circle_shape(self, x, y, radius):
        circle = Circle([(x, y)], radius)
        circle.draw(self.ax)
        self.shapes.append(circle)
        self.update_display()
        self.update_label()

    def run(self):
        plt.show()

    def update_display(self):
        self.ax.cla()

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')  # Set the aspect ratio to 'equal'
        self.ax.grid(True)

        for shape in self.shapes:
            shape.draw(self.ax)

        plt.draw()


    def update_label(self):
        global label_text
        for widget in self.label_widgets:
            widget.destroy()
        self.label_widgets = []

        for shape in self.shapes:
            if isinstance(shape, Point):
                label_text = f'Point: ({shape.coords[0][0][0]:.1f}, {shape.coords[0][0][1]:.1f})'

            elif isinstance(shape, Circle):
                x, y = shape.coords[0]
                r = shape.radius
                label_text = f'Circle: (x-{x:.1f})^2 + (y-{y:.1f})^2 = {r**2:.1f}'

            elif isinstance(shape, Line):
                label_text = f'Line: y = {shape.m:.1f}x + {shape.b:.1f}'

            label_widget = tk.Label(self.side_panel.text, text=label_text, bg='white')
            label_widget.pack(anchor='w')
            self.label_widgets.append(label_widget)





window = MainWindow()
#cid = window.ax.figure.canvas.mpl_connect('button_press_event', window.handle_input)
window.run()