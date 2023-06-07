import matplotlib.pyplot as plt
import numpy as np

import config
from Shapes.Circle import Circle
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Polygon import Polygon
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
        self.p = ax.plot(self.x, self.y, 'ro')
        plt.annotate(self.label, (self.x, self.y))

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
        self.x=x
        self.y=y

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, bool):
        self.hidden = bool

    def get_label(self):
        return self.label

    def is_line_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        flag = False
        for shape in shapes:
            if isinstance(shape, Line):
                if shape.get_start() == self or shape.get_end() == self:
                    flag = shape
        return flag

    def is_segment_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        flag = False
        for shape in shapes:
            if isinstance(shape, Segment):
                if shape.get_start() == self or shape.get_end() == self:
                    flag = shape
        return flag

    def is_circle_part(self, shapes=None):
        if shapes is None:
            shapes = config.shapes
        flag = False
        for shape in shapes:
            if isinstance(shape, Circle):
                if shape.get_center() == self:
                    flag = shape
        return flag
    
    def is_polygon_part(self, shapes=None):
        segments_part=[]
        if shapes is None:
            shapes = config.shapes
        for shape in shapes:
            if isinstance(shape, Polygon):
                for segment in shape.get_segment_list():
                    if segment.get_start() == self or segment.get_end() == self:
                        return shape
                        # segments_part.append(segment)
                        # if len(segments_part) == 2:
                        #     return segments_part
                        
        # print(segments_part)
        return False

    def is_in_poly(self, poly):
        for segment in poly.get_segment_list():
            if segment.get_start() == self or segment.get_end() == self:
                return True
        return False
    
    def area(self) -> float:
        return 0

    def perimeter(self) -> float:
        return 0

    def convex_hull(self):
        return self

   


