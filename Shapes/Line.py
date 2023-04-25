import math

import numpy as np
from Shapes.shapes import Shape
from matplotlib.axes import Axes
#
# class Line(Shape):
#     def __init__(self, m, b):
#         self.m = m
#         self.b = b
#         self.line_obj = None
#
#     def draw(self, ax: Axes):
#         x = np.linspace(-10, 10, 100)
#         y = self.m * x + self.b
#         self.line_obj, = ax.plot(x, y)  # Store the line object
import config

class Line(Shape):
    def __init__(self, p1, p2):

        self.x1 = p1.coords[0][0]
        self.y1 = p1.coords[0][1]
        self.x2 = p2.coords[0][0]
        self.y2 = p2.coords[0][1]
        self.line_obj = None
        self.dashes_obj = None
        self.update_line_and_dashes()

    def m_b(self):
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - m * self.x1
        return m, b

    def draw(self, ax: Axes):
        m, b = self.m_b()
        # draw_line_shape(m, b)
        x_range = np.array([-100, 1000])
        self.line_obj, = config.ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-', linewidth=2)

        # Draw the dashed lines on either side of the solid line

        self.dashes_obj, = config.ax.plot(x_range, m * x_range + b, linestyle='--', linewidth=1, color='black')

    # def update_line_and_dashes(self):
    #     self.draw(config.ax)
    #     m, b = self.m_b()
    #     x_range = np.array([-100, 1000])
    #     self.line_obj.set_data([self.x1, self.x2], [self.y1, self.y2])
    #     self.dashes_obj.set_data(x_range, m * x_range + b)
    #     config.fig.canvas.draw_idle()

    def update_line_and_dashes(self):
        m, b = self.m_b()
        x_range = np.array([-100, 1000])

        if self.line_obj:
            self.line_obj.pop(0).remove()  # remove old line
        self.line_obj = config.ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-',
                                       linewidth=2)

        if self.dashes_obj:
            self.dashes_obj.pop(0).remove()  # remove old dashed line
        self.dashes_obj, = config.ax.plot(x_range, m * x_range + b, linestyle='--', linewidth=1, color='black')

        config.fig.canvas.draw_idle()













