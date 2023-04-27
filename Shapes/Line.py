import math

import numpy as np

from Shapes.Point import Point
from Shapes.shapes import Shape
from matplotlib.axes import Axes
import config


class Line(Shape):
    def __init__(self, p1, p2, label):
        self.p1 = p1
        self.x1 = p1.coords[0][0]
        self.y1 = p1.coords[0][1]

        self.p2 = p2
        self.x2 = p2.coords[0][0]
        self.y2 = p2.coords[0][1]
        self.line_obj = None
        self.dashes_obj = None

        self.label = label
        # self.update_line_and_dashes()

    def m_b(self):
        try:
            m = (self.y2 - self.y1) / (self.x2 - self.x1)
            b = self.y1 - m * self.x1
            return m, b

        except RuntimeWarning:
            b = self.y1
            return 0.000, b

    def draw(self, ax: Axes):
        m, b = self.m_b()
        # draw_line_shape(m, b)
        x_range = np.array([-100, 1000])
        self.line_obj, = ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-', linewidth=2)

        # Draw the dashed lines on either side of the solid line

        self.dashes_obj, = ax.plot(x_range, m * x_range + b, linestyle='-', linewidth=1, color='black')
        #self.update_line_and_dashes()

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
        self.line_obj, = config.ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-',
                                       linewidth=2)

        if self.dashes_obj:
            self.dashes_obj.pop(0).remove()  # remove old dashed line
        self.dashes_obj, = config.ax.plot(x_range, m * x_range + b, linestyle='--', linewidth=1, color='black')

        config.fig.canvas.draw_idle()

    def get_start_point(self):
        return round(self.x1, 3), round(self.y1, 3)

    def get_end_point(self):
        return round(self.x2, 3), round(self.y2, 3)

    def get_start(self):
        return self.p1

    def get_end(self):
        return self.p2

    def set_start_point(self, x, y):
        self.x1 += x
        self.y1 += y
        self.p1.set_x(x)
        self.p1.set_y(y)

    def set_end_point(self, x, y):
        self.x2 += x
        self.y2 += y
        self.p2.set_x(x)
        self.p2.set_y(y)

    def is_line_edge(self, p):
        if round(p.get_x(), 2) == round(self.x1, 2) and round(p.get_y(), 2) == round(self.y1, 2):
            return True, "start"
        elif round(p.get_x(), 2) == round(self.x2, 2) and round(p.get_y(), 2) == round(self.y2, 2):
            return True, "end"

        return False, False

    # def __repr__(self):
    #     return "Line"

    def get_label(self):
        return self.label
