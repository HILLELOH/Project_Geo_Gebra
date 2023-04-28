import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class Shape:
    def __init__(self,coords):
        self.coords= np.array(coords)
    
    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'data': self._serialize()
        }

    @classmethod
    def deserialize(cls, shape_data):
        shape_type = shape_data['type']
        shape_data = shape_data['data']

        if shape_type == 'Point':
            return Point._deserialize(shape_data)
        elif shape_type == 'Line':
            return Line._deserialize(shape_data)
        elif shape_type == 'Circle':
            return Circle._deserialize(shape_data)
        else:
            raise ValueError(f'Unknown shape type: {shape_type}')
        
class Point(Shape):
    def __init__(self,coords):
        super().__init__([coords])
    def draw(self,ax:Axes):
        ax.plot(*self.coords.T,'ro')
    
    def __str__(self):
        return f"({list(self.coords)[0][0][0]:0.2f} , {list(self.coords)[0][0][1]:0.2f})"
    
    def _serialize(self):
        return {
            'coords': self.coords.tolist()
        }

    @staticmethod
    def _deserialize(data):
        return Point(np.array(data['coords']).reshape(1, 2))
    
class Line(Shape):
    def __init__(self, m, b, point1, point2):
        self.m = m
        self.b = b
        self.line_obj = None
        self.point1 = point1
        self.point2 = point2

    def draw(self, ax: Axes):
        x = np.linspace(-10, 10, 100)
        y = self.m * x + self.b
        self.line_obj, = ax.plot(x, y)  # Store the line object
    
    def _serialize(self):
        return {
            'point1': self.point1.serialize(),
            'point2': self.point2.serialize(),
            'm': self.m,
            'b': self.b,
        }

    @staticmethod
    def _deserialize(data):
        return Line(data['m'], data['b'], Point.deserialize(data['point1']), Point.deserialize(data['point2']))


        
class Circle(Shape):
    def __init__(self, coords, radius, point1_coords, point2_coords):  # Add point1_coords and point2_coords as arguments
        super().__init__(coords)
        self.radius = radius
        self.center_point = Point(coords)
        self.point1 = Point(point1_coords)  # Create point1
        self.point2 = Point(point2_coords)  # Create point2

    def draw(self, ax):
        circle = plt.Circle(self.coords[0], self.radius, fill=False)
        ax.add_artist(circle)
        self.point1.draw(ax)  # Draw point1
        self.point2.draw(ax)  # Draw point2
        
    def _serialize(self):
        return {
            'coords': self.coords.tolist(),
            'radius': self.radius,
            'point1': self.point1.serialize(),
            'point2': self.point2.serialize()
        }
    @staticmethod
    def _deserialize(data):
        return Circle(np.array(data['coords']), data['radius'], Point.deserialize(data['point1']), Point.deserialize(data['point2']))

class Polygon:
    def __init__(self, coords):
        self.coords = coords

    def draw(self, ax):
        x, y = zip(*self.coords)
        ax.plot(x, y, 'k-')