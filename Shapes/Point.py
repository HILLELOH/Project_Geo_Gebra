import matplotlib.pyplot as plt

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
