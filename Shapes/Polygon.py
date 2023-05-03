from typing import List, Tuple

import numpy as np
from matplotlib.axes import Axes
from scipy.spatial import ConvexHull, Delaunay

import config
from Shapes.Line import Line
from Shapes.Point import Point
from Shapes.Segment import Segment
from Shapes.shapes import Shape


class Polygon(Shape):
    def __init__(self, segments_list, label):
        self.segments_list = segments_list
        self.label = label
        self.hidden = True

    def draw(self, ax: Axes):
        for segment in self.segments_list:
            m, b = segment.m_b()
            # draw_line_shape(m, b)
            x_range = np.array([-100, 1000])
            start = segment.get_start()
            end = segment.get_end()
            segment.set_segment_obj(ax.plot([start.get_x(), end.get_x()], [start.get_y(), end.get_y()], color='black', linestyle='-', linewidth=2))
            # segment.dashes_obj, = ax.plot(x_range, m * x_range + b, linestyle='-', linewidth=1, color='black')

    def add_segment(self, segment):
        self.segments_list.append(segment)

    def get_segment_list(self):
        return self.segments_list

    def get_label(self):
        return self.label

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b

    def area(self) -> float:
        '''
        The 'area' function calculates the area of the polygon using the shoelace formula. It first extracts the
        x-coordinates and y-coordinates of the polygon vertices from the line objects, and then calculates the area
        using the formula: A = 1/2 * | x1*y2 + x2*y3 + ... + xn-1*yn + xn*y1 - y1*x2 - y2*x3 - ... - yn-1*xn - yn*x1 |
        :return: Area of the current 'Polygon' object
        '''
        x = [segment.get_start().get_x() for segment in self.segments_list] + [self.segments_list[-1].get_end().get_x()]
        y = [segment.get_start().get_y() for segment in self.segments_list] + [self.segments_list[-1].get_end().get_y()]
        area = 0.0
        j = len(x) - 1
        for i in range(len(x)):
            area += (x[j] + x[i]) * (y[j] - y[i])
            j = i
        return abs(area / 2.0)

    def perimeter(self) -> float:
        '''
        The 'perimeter' function iterates through all the lines in the polygon, calculates the length of each line using
        the 'perimeter' method from the 'Line' class, and adds it to the perimeter variable.
        :return: total perimeter of the current 'Polygon' object.
        '''
        perimeter = 0.0
        for segment in self.segments_list:
            perimeter += segment.perimeter()
        return perimeter

    def convex_hull(self):
        '''
        This method calculates the convex hull of the current polygon and returns it as a new 'Polygon' object.
        To do this, we first create a list of all the points in the polygon by iterating over all the lines in the
        polygon and adding the start and end points of each line to the list. We then pass this list of points to the
        'ConvexHull' function from the 'scipy.spatial' module to calculate the convex hull. Finally, we create a new
        list of lines that form the convex hull by iterating over the simplices in the convex hull and creating a new
        'Line' object for each one.
        :return: New 'Polygon' object that represents the convex hull of the current polygon.
        '''
        points = [] # Get a list of all the points in the polygon
        for segment in self.segments_list:
            start = segment.get_start()
            end = segment.get_end()
            points.append([start.get_x(), start.get_y()])
            points.append([end.get_x(), end.get_y()])
        hull = ConvexHull(points) # Calculate the convex hull of the points
        hull_segments = [] # Create a list of segments that form the convex hull
        for simplex in hull.simplices:
            start = simplex[0]
            end = simplex[1]
            x1, y1 = points[start]
            x2, y2 = points[end]
            hull_segments.append(Segment(Point(x1, y1), Point(x2, y2)))
        return Polygon(hull_segments, self.label)

    def is_convex(self) -> bool:
        '''
        The 'is_convex' function determines whether the polygon is convex or not. A polygon is convex if all its interior
        angles are less than 180 degrees. We iterate over all the vertices of the polygon and calculate the cross product
        of the vectors formed by adjacent edges. If the sign of the cross product changes for any adjacent edge, then the
        polygon is not convex. If the sign of the cross product remains the same for all adjacent edges, then the polygon
        is convex.
        :return: True if the polygon is convex, False otherwise.
        '''
        num_vertices = len(self.segments_list)
        if num_vertices < 3:
            return False
        sign = None
        for i in range(num_vertices):
            p1 = self.segments_list[i].get_start()
            p2 = self.segments_list[(i + 1) % num_vertices].get_start()
            p3 = self.segments_list[(i + 2) % num_vertices].get_start()
            cross_product = (p2.get_x() - p1.get_x()) * (p3.get_y() - p2.get_y()) - (p2.get_y() - p1.get_y()) * (
                        p3.get_x() - p2.get_x())
            if sign is None:
                sign = np.sign(cross_product)
            elif np.sign(cross_product) != sign:
                return False
        return True

    def triangulate(self) -> List[Tuple[int, int, int]]:
        """
        Triangulate the polygon into a list of triangles using the Delaunay triangulation method.
        :return: A list of tuples, where each tuple contains the indices of the vertices of a triangle.
        """
        vertices = np.array([segment.get_start().to_array() for segment in self.segments_list]) # Get the polygon vertices as a numpy array
        tri = Delaunay(vertices) # Compute the Delaunay triangulation of the vertices
        triangles = [] # Create a list of tuples representing the triangles in the triangulation
        for indices in tri.simplices:
            triangles.append(tuple(indices))

        return triangles
