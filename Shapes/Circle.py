import math
from Shapes.shapes import Shape

from matplotlib.axes import Axes
from matplotlib import pyplot as plt


class Circle(Shape):
    def __init__(self, center, radius, label):
        super().__init__((center.get_x(), center.get_y()))
        self.center = center
        self.radius = radius
        self.label = label

    def draw(self, ax: Axes):
        x, y = self.coords[0]
        circle = plt.Circle((x, y), self.radius, fill=False)
        ax.add_patch(circle)

    def getShape(self):
        return f'{Circle}'

    def get_label(self):
        return self.label
