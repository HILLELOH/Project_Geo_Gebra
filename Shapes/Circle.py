import math

import config
from Shapes.shapes import Shape

from matplotlib.axes import Axes
from matplotlib import pyplot as plt


class Circle(Shape):
    def __init__(self, center, radius, label):
        super().__init__((center.get_x(), center.get_y()))
        self.center = center
        self.radius = radius
        self.label = label
        self.circle_object = None
        self.hidden = False

    # def draw(self, ax: Axes):
    #     x = self.center.get_x()
    #     y = self.center.get_y()
    #     circle = plt.Circle((x, y), self.radius, fill=False)
    #     ax.add_patch(circle)

    def draw(self, ax: Axes):
        x = self.center.get_x()
        y = self.center.get_y()
        self.circle_object = plt.Circle((x, y), self.radius, fill=False)
        ax.add_patch(self.circle_object)

    def update_line_and_dashes(self):
        x = self.center.get_x()
        y = self.center.get_y()
        if self.circle_object:
            self.circle_object.pop(0).remove()  # remove old line
        self.circle_object = plt.Circle((x, y), self.radius, fill=False)
        config.ax.add_patch(self.circle_object)

        config.fig.canvas.draw_idle()


    def getShape(self):
        return f'{Circle}'

    def get_label(self):
        return self.label

    def get_center(self):
        return self.center

    def set_center(self, x, y):
        self.center.set_x(x)
        self.center.set_y(y)


    def get_radius(self):
        return self.radius

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b

    def area(self) -> float:
        a = math.pi * (self.radius ** 2)
        return a

    def perimeter(self) -> float:
        p = 2 * math.pi * self.radius
        return p

    def convex_hull(self):
        return self