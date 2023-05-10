
import math
import logging
from logging import debug
import numpy as np
from Shapes.Polygon import Polygon

r = logging.getLogger()
r.setLevel(logging.DEBUG)

from Shapes.shapes import Shape
from matplotlib.axes import Axes
import config


class Segment(Shape):
    def __init__(self, p1, p2, label):
        self.p1 = p1
        self.x1 = p1.coords[0][0]
        self.y1 = p1.coords[0][1]

        self.p2 = p2
        self.x2 = p2.coords[0][0]
        self.y2 = p2.coords[0][1]
        self.segment_obj = None
        self.hidden = False
        self.label = label
        # self.update_line_and_dashes()

    def m_b(self):
        try:
            # debug(f'\n p1: ({self.x1}, {self.y1})\n p2: ({self.x2}, {self.y2})')
            m = (self.y2 - self.y1) / (self.x2 - self.x1)
            b = self.y1 - m * self.x1
            return m, b

        except RuntimeWarning:
            debug(f'p1: ({self.x1}, {self.y1})\n p2: ({self.x2}, {self.y2})')
            b = self.y1
            return 0.000, b

    def draw(self, ax: Axes):
        self.segment_obj, = ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-', linewidth=2)

    def update_line_and_dashes(self):
        if self.segment_obj:
            self.segment_obj.pop(0).remove()  # remove old line
        self.segment_obj, = config.ax.plot([self.x1, self.x2], [self.y1, self.y2], color='black', linestyle='-',
                                           linewidth=2)
        config.fig.canvas.draw_idle()


    def is_polygon_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        flag = False
        for shape in shapes:
            if isinstance(shape, Polygon):
                if self in shape.get_segment_list():
                    flag = shape
        return flag

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

    def is_segment_edge(self, p):
        if round(p.get_x(), 2) == round(self.x1, 2) and round(p.get_y(), 2) == round(self.y1, 2):
            return True, "start"
        elif round(p.get_x(), 2) == round(self.x2, 2) and round(p.get_y(), 2) == round(self.y2, 2):
            return True, "end"

        return False, False

    # def __repr__(self):
    #     return "Line"

    def get_label(self):
        return self.label

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b

    def set_segment_obj(self, dash):
        self.segment_obj = dash
