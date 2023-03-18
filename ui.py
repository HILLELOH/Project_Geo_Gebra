import matplotlib.pyplot as plt
from shapes import *
import tkinter as tk
import numpy as np

class MainWindow:
    def __init__(self):
        # Create the squared XY plane
        fig, ax = plt.subplots()

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

        # Set the grid lines to be visible
        ax.grid(True)

        self.ax = ax

        # Empty list of shapes
        self.shapes = []

        # Create buttons for drawing points and lines
        self.point_button = tk.Button(text="Draw Point", command=self.draw_point)
        self.point_button.pack(side="left", padx=10, pady=10)

        self.line_button = tk.Button(text="Draw Line", command=self.draw_line)
        self.line_button.pack(side="left", padx=10, pady=10)

        self.label = tk.Label(text="", font=("Arial", 14))
        self.label.pack(side="left", padx=10, pady=10)

        self.cid = None
    def draw_point(self):
        # Bind the handle_input method to the canvas when drawing points
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.handle_input_point)

    def draw_line(self):
        # Bind the handle_input method to the canvas when drawing lines
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.handle_input_line)

    def handle_input_point(self, event):
        if event.button == 1:  # Left mouse button
            x, y = event.xdata, event.ydata
            self.draw_point_shape(x, y)
            # Disconnect the event listener so points can't be drawn anymore
            self.ax.figure.canvas.mpl_disconnect(self.cid)

    def handle_input_line(self, event):
        if event.button == 2:  # Left mouse button
            x1, y1 = event.xdata, event.ydata
            plt.title("Click left click to draw a line")
            plt.draw()
            event2 = plt.ginput(1, timeout=-1)[0]
            x2, y2 = event2[0], event2[1]
            self.draw_line_shape(x1, y1, x2, y2)
            # Disconnect the event listener so lines can't be drawn anymore
            self.ax.figure.canvas.mpl_disconnect(self.cid)

    def draw_point_shape(self, x, y):
        point = Point([(x, y)])
        point.draw(self.ax)
        self.shapes.append(point)
        self.update_display()
        self.update_label()

    def draw_line_shape(self, x1, y1, x2, y2):
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        x = np.linspace(-10, 10, 100)
        y = m * x + b
        line = Line(m, b)

        line.draw(self.ax)

        self.shapes.append(line)
        self.update_display()
        self.update_label()

    def run(self):
        plt.show()

    def update_display(self):
        self.ax.cla()

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.grid(True)

        for shape in self.shapes:
            shape.draw(self.ax)

        plt.draw()

    def update_label(self):
        self.label.config(text="")
        coords = [f"(x={list(p.coords)[0][0][0]:0.2f} , y={list(p.coords)[0][0][1]:0.2f})" for p in self.shapes if isinstance(p, Point)]
        last_shape = self.shapes[-1] if len(self.shapes) > 0 else None
        if isinstance(last_shape, Line):
            m = last_shape.m
            b = last_shape.b
            equation_str = f"y = {m:.2f}x + {b:.2f}"
            coords.append(equation_str)
        self.label.config(text="\n".join(coords) + "\n" + self.label.cget("text"))
        

window = MainWindow()
#cid = window.ax.figure.canvas.mpl_connect('button_press_event', window.handle_input)
window.run()