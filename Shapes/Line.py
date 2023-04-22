import math

import numpy as np
from Shapes.shapes import Shape
from matplotlib.axes import Axes

class Line(Shape):
    def __init__(self, m, b):
        self.m = m
        self.b = b
        self.line_obj = None

    def draw(self, ax: Axes):
        x = np.linspace(-10, 10, 100)
        y = self.m * x + self.b
        self.line_obj, = ax.plot(x, y)  # Store the line object

    def getShape(self):
        return f'{Line}'










