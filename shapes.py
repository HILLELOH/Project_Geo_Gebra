import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class Shape:
    def __init__(self,coords):
        self.coords= np.array(coords)
        
class Point(Shape):
    def __init__(self,coords):
        super().__init__([coords])
    def draw(self,ax:Axes):
        ax.plot(*self.coords.T,'ro')
    
    def __str__(self):
        return f"({list(self.coords)[0][0][0]:0.2f} , {list(self.coords)[0][0][1]:0.2f})"
    
class Line(Shape):
    def __init__(self, m, b):
        self.m = m
        self.b = b
        self.line_obj = None

    def draw(self, ax: Axes):
        x = np.linspace(-10, 10, 100)
        y = self.m * x + self.b
        self.line_obj, = ax.plot(x, y)  # Store the line object


        
class Circle(Shape):
    def __init__(self, coords, radius):
        super().__init__(coords)
        self.radius = radius

    def draw(self, ax: Axes):
        x, y = self.coords[0]
        circle = plt.Circle((x, y), self.radius, fill=False)
        ax.add_patch(circle)
