import matplotlib.pyplot as plt
import numpy as np

import config
from Shapes.Circle import Circle
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.shapes import Shape
from matplotlib.axes import Axes


class Point(Shape):
    def __init__(self, x, y, label):
        super().__init__([[x, y]])
        self.x = x
        self.y = y
        self.label = label
        self.hidden = False
        self.p = None

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def draw(self, ax: Axes):
        self.p = ax.plot(self.x, self.y, 'o', color='#ff6b8a', markersize=6, zorder=5)
        plt.annotate(
            self.label, (self.x, self.y),
            color='#ff6b8a',
            fontsize=9,
            xytext=(5, 5),
            textcoords='offset points',
        )

    def set_color(self, color):
        self.p[0].set_color(color)

    def __str__(self):
        return f"({self.x:0.3f} , {self.y:0.3f})"

    def __repr__(self):
        return f"({self.x:0.3f} , {self.y:0.3f})"

    def set_x(self, x):
        self.x += x

    def set_y(self, y):
        self.y += y

    def set_p(self, x, y):
        self.x = x
        self.y = y

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b

    def get_label(self):
        return self.label

    def is_line_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        for shape in shapes:
            if isinstance(shape, Line):
                if shape.get_start() is self or shape.get_end() is self:
                    return shape
        return False

    def is_segment_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        for shape in shapes:
            if isinstance(shape, Segment):
                if shape.get_start() is self or shape.get_end() is self:
                    return shape
        return False

    def is_circle_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        for shape in shapes:
            if isinstance(shape, Circle):
                if shape.get_center() is self:
                    return shape
        return False

    def is_polygon_part(self, shapes=None):
        from Shapes.Polygon import Polygon  # lazy import — breaks circular dependency
        if shapes is None:
            shapes = config.shapes
        for shape in shapes:
            if isinstance(shape, Polygon):
                for seg in shape.get_segment_list():
                    if seg.get_start() is self or seg.get_end() is self:
                        return shape
        return False

    def is_in_poly(self, poly):
        for seg in poly.get_segment_list():
            if seg.get_start() is self or seg.get_end() is self:
                return True
        return False

    def area(self) -> float:
        return 0

    def perimeter(self) -> float:
        return 0

    def convex_hull(self):
        return self
