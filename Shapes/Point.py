import matplotlib.pyplot as plt

import config
from Shapes.Circle import Circle
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Polygon import Polygon
from Shapes.shapes import Shape
from matplotlib.axes import Axes


class Point(Shape):
    def __init__(self, coords, label):
        self.x = coords[0]
        self.y = coords[1]
        super().__init__([coords])
        self.label = label
        self.hidden = False

    def draw(self, ax: Axes):
        ax.plot(*self.coords.T, 'ro')
        plt.annotate(self.label, (self.x, self.y))

    def __str__(self):
        return f"({self.x:0.3f} , {self.y:0.3f})"

    def getShape(self):
        return f'{Point}'

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x += x

    def set_y(self, y):
        self.y += y

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
                for segment in shape.get_segments():
                    if segment.get_start() == self or segment.get_end() == self:
                        segments_part.append(segment)
                        if len(segments_part) == 2:
                            return segments_part
                        
        print(segments_part)
        return False

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, bool):
        self.hidden = bool


