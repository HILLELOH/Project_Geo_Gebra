
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
        self.p2 = p2
        self.label = label
        self.hidden = False

        self.segment_obj = None

    def m_b(self):
        try:
            m = (self.p2.get_y() - self.p1.get_y()) / (self.p2.get_x() - self.p1.get_x())
            b = self.p1.get_y() - m * self.p1.get_x()
            return m, b

        except RuntimeWarning:
            return 0, 0

    def draw(self, ax: Axes):
        self.segment_obj, = ax.plot([self.p1.get_x(), self.p2.get_x()], [self.p1.get_y(), self.p2.get_y()], color='black', linestyle='-', linewidth=2)


    def is_polygon_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        flag = False
        for shape in shapes:
            if isinstance(shape, Polygon):
                if self in shape.get_segment_list():
                    flag = shape
        return flag

    def get_start(self):
        return self.p1

    def get_end(self):
        return self.p2

    def set_start_point(self, x, y):
        self.p1.set_x(x)
        self.p1.set_y(y)

    def set_end_point(self, x, y):
        self.p2.set_x(x)
        self.p2.set_y(y)

    def get_label(self):
        return self.label

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b
