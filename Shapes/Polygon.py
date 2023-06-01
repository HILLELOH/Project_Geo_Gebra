import numpy as np
from matplotlib.axes import Axes

import config
from Shapes.Point import *
from Shapes.shapes import Shape

from scipy.spatial import ConvexHull, Delaunay
from math import atan2


class Polygon:
    def __init__(self, segment_list, label):
        self.segment_list = segment_list
        self.label = label
        self.hidden = True

    def draw(self, ax: Axes):
        for segment in self.segment_list:
            # m, b = segment.m_b()
            # # draw_line_shape(m, b)
            # x_range = np.array([-100, 1000])
            start = segment.get_start()
            end = segment.get_end()
            segment.set_segment_obj(ax.plot([start.get_x(), end.get_x()], [start.get_y(), end.get_y()], color='black', linestyle='-', linewidth=2))
            # line.dashes_obj, = ax.plot(x_range, m * x_range + b, linestyle='-', linewidth=1, color='black')

    def add_segment(self, segment):
        self.segment_list.append(segment)

    def get_segment_list(self):
        return self.segment_list

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
        x = [segment.get_start().get_x() for segment in self.segment_list] + [self.segment_list[-1].get_end().get_x()]
        y = [segment.get_start().get_y() for segment in self.segment_list] + [self.segment_list[-1].get_end().get_y()]
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
        for segment in self.segment_list:
            perimeter += segment.perimeter()
        return perimeter

    def polar_angle(self, p1, p2):
        return atan2(p2.y - p1.y, p2.x - p1.x)

    def find_lowest_point(self, points):
        lowest_point = points[0]
        for point in points:
            if point.y < lowest_point.y:
                lowest_point = point
            elif point.y == lowest_point.y and point.x < lowest_point.x:
                lowest_point = point
        return lowest_point

    def orientation(self, p, q, r):
        value = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if value == 0:
            return 0  # Collinear points
        elif value > 0:
            return 1  # Clockwise orientation
        else:
            return 2  # Counterclockwise orientation

    def graham_scan(self, points):
        n = len(points)
        if n < 3:
            return []  # Not enough points to form a convex hull

        lowest_point = self.find_lowest_point(points)
        sorted_points = sorted(points, key=lambda p: self.polar_angle(lowest_point, p))

        stack = [lowest_point, sorted_points[0], sorted_points[1]]

        for i in range(2, n):
            while len(stack) > 1 and self.orientation(stack[-2], stack[-1], sorted_points[i]) != 2:
                stack.pop()
            stack.append(sorted_points[i])

        segments = []
        for i in range(len(stack) - 1):
            p1, p2 = stack[i], stack[i + 1]
            segments.append(Segment(p1, p2, ''))

        p1, p2 = stack[-1], stack[0]
        segments.append(Segment(p1, p2, ''))

        return segments



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
        from Shapes.Point import Point
        from Shapes.Segment import Segment
        points = []  # Get a list of all the points in the polygon
        for segment in self.segment_list:
            start = segment.get_start()
            end = segment.get_end()
            points.append([start.get_x(), start.get_y()])
            points.append([end.get_x(), end.get_y()])
            # if start not in points:
            #     points.append(start)
            # if end not in points:
            #     points.append(end)

        hull = ConvexHull(points)  # Calculate the convex hull of the points
        hull_segments = []  # Create a list of segments that form the convex hull
        for simplex in hull.simplices:
            start = simplex[0]
            end = simplex[1]
            x1, y1 = points[start]
            x2, y2 = points[end]
            # for seg in config.shapes:
            #     if isinstance(seg, Segment):
            #         if seg.get_start().get_x()
            hull_segments.append(
                Segment(Point(x1, y1, ''), Point(x2, y2, ''), ''))
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
        num_vertices = len(self.segment_list)
        if num_vertices < 3:
            return False
        sign = None
        for i in range(num_vertices):
            p1 = self.segment_list[i].get_start()
            p2 = self.segment_list[(i + 1) % num_vertices].get_start()
            p3 = self.segment_list[(i + 2) % num_vertices].get_start()
            cross_product = (p2.get_x() - p1.get_x()) * (p3.get_y() - p2.get_y()) - (p2.get_y() - p1.get_y()) * (
                    p3.get_x() - p2.get_x())
            if sign is None:
                sign = np.sign(cross_product)
            elif np.sign(cross_product) != sign:
                return False
        return True

    def triangulate(self):
        """
        Triangulate the polygon into a list of triangles using the Delaunay triangulation method.
        :return: A list of tuples, where each tuple contains the indices of the vertices of a triangle.
        """
        vertices = []  # List to store the polygon vertices
        for segment in self.segment_list:
            vertices.append(segment.p1)
            vertices.append(segment.p2)

        vertices_array = np.array([[point.x, point.y] for point in vertices])
        tri = Delaunay(vertices_array)  # Compute the Delaunay triangulation of the vertices
        triangles = []
        for indices in tri.simplices:
            triangle = (vertices[indices[0]], vertices[indices[1]], vertices[indices[2]])
            triangles.append(triangle)
        return triangles


        # vertices = np.array([segment.get_start().to_array() for segment in
        #                      self.segment_list])  # Get the polygon vertices as a numpy array
        # tri = Delaunay(vertices)  # Compute the Delaunay triangulation of the vertices
        # triangles = []  # Create a list of tuples representing the triangles in the triangulation
        # for indices in tri.simplices:
        #     triangles.append(tuple(indices))
        #
        # return triangles
