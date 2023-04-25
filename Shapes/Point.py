from Shapes.shapes import Shape
from matplotlib.axes import Axes

class Point(Shape):
    def __init__(self, coords):
        super().__init__([coords])

    def draw(self, ax: Axes):
        ax.plot(*self.coords.T, 'ro')

    def __str__(self):
        return f"({list(self.coords)[0][0][0]:0.3f} , {list(self.coords)[0][0][1]:0.3f})"

    def getShape(self):
        return f'{Point}'
