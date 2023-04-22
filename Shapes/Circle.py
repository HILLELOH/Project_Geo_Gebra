import math
from Shapes.shapes import Shape

from matplotlib.axes import Axes
from matplotlib import pyplot as plt

class Circle(Shape):
    def __init__(self, coords, radius):
        super().__init__(coords)
        self.radius = radius

    def draw(self, ax: Axes):
        x, y = self.coords[0]
        circle = plt.Circle((x, y), self.radius, fill=False)
        ax.add_patch(circle)

    def getShape(self):
        return f'{Circle}'