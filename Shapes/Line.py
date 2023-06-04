import math

import numpy as np


from Shapes.shapes import Shape
from matplotlib.axes import Axes
import config


class Line(Shape):
    def __init__(self, p1, p2, label):
        self.p1 = p1
        self.p2 = p2
        self.label = label
        self.hidden = False

        self.line_obj = None
        self.dashes_obj = None

    def m_b(self):
        if self.p2.get_x() - self.p1.get_x() == 0:
            return 1, 0

        m = (self.p2.get_y() - self.p1.get_y()) / (self.p2.get_x() - self.p1.get_x())
        b = self.p1.get_y() - m * self.p1.get_x()
        return m, b



    def draw(self, ax: Axes):
        self.line_obj = ax.axline((self.p1.get_x(), self.p1.get_y()), (self.p2.get_x(), self.p2.get_y()), color='black', label='by points')
        # ax.legend()

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
        
    def area(self) -> float:
        return 0

    def perimeter(self) -> float:
        distance = math.sqrt((self.p2.get_x() - self.p1.get_x()) ** 2 + (self.p2.get_y() - self.p1.get_y()) ** 2)
        return distance

    def convex_hull(self):
        return self

