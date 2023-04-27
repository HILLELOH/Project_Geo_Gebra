import matplotlib.pyplot as plt

import config
from Shapes.Line import Line
from Shapes.shapes import Shape
from matplotlib.axes import Axes


class Point(Shape):
    def __init__(self, coords, label):
        self.x = coords[0]
        self.y = coords[1]
        super().__init__([coords])
        self.label = label

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

    def is_line_part(self):
        flag = False
        for shape in config.shapes:
            if isinstance(shape, Line):
                start = shape.get_start()
                end = shape.get_end()
                if round(start.get_x(), 2) == round(self.x, 2) and round(start.get_y(), 2) == round(self.y, 2):
                    flag = True

                elif round(end.get_x(), 2) == round(self.x, 2) and round(end.get_y(), 2) == round(self.y, 2):
                    flag = True
        return flag
