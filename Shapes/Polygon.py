import math

import numpy as np
from matplotlib.axes import Axes

import config
from Shapes.Point import *
from Shapes.Triangle import Triangle
from Shapes.shapes import Shape
from Shapes.Segment import Segment

from scipy.spatial import ConvexHull, Delaunay
from math import atan2


class Polygon:
    def __init__(self, segment_list, label):
        self.segment_list = segment_list
        self.label = label
        self.hidden = True

    def draw(self, ax: Axes):
        # for segment in self.segment_list:
        #     start = segment.get_start()
        #     end = segment.get_end()
        #     segment.set_segment_obj(
        #         ax.plot([start.get_x(), end.get_x()], [start.get_y(), end.get_y()], color='black', linestyle='-',
        #                 linewidth=2))
        pass

    def add_segment(self, segment):
        self.segment_list.append(segment)

    def get_segment_list(self):
        return self.segment_list

    def get_label(self):
        return self.label

    def set_label(self, label):
        if self.label=="":
            self.label = label

        else:
            self.label = f'{self.label},{label}'

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
        return atan2(p2.get_y() - p1.get_y(), p2.get_x() - p1.get_x())

    def find_lowest_point(self, points):
        lowest_point = points[0]
        for point in points:
            if point.get_y() < lowest_point.get_y():
                lowest_point = point
            elif point.get_y() == lowest_point.get_y() and point.get_x() < lowest_point.get_x():
                lowest_point = point
        return lowest_point

    def orientation(self, p, q, r):
        value = (q.get_y() - p.get_y()) * (r.get_x() - q.get_x()) - (q.x - p.get_x()) * (r.get_y() - q.get_y())
        if value == 0:
            return 0  # Collinear points
        elif value > 0:
            return 1  # Clockwise orientation
        else:
            return 2  # Counterclockwise orientation

    def find_point(self, points, coords):
        for point in points:
            if point.get_x() == coords[0] and point.get_y() == coords[1]:
                return point
        return None


    def set_color(self, color):
        for seg in self.segment_list:
            seg.set_color(color)
            seg.get_start().set_color(color)

    def graham_scan(self, points):
        n = len(points)
        if n < 3:
            return []  # Not enough points to form a convex hull
        coords = []
        for point in points:
            coords.append([point.get_x(), point.get_y()])
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
            print(type(p1))
            segments.append(Segment(p1, p2, ''))
        p1, p2 = stack[-1], stack[0]
        segments.append(Segment(p1, p2, ''))
        return segments

    def triangulation(self):
        '''
        When triangulating a polygon using the Delaunay method, the new edges can be created both inside and outside the
        polygon.
        :return:
        '''
        points = []  # Get a list of all the points in the polygon
        for segment in self.segment_list:
            start = segment.get_start()
            # end = segment.get_end()
            points.append([start.get_x(), start.get_y()])
            # points.append([end.get_x(), end.get_y()])
        # vertices = np.array([segment.get_start().to_array() for segment in
        #                      self.segment_list])  # Get the polygon vertices as a numpy array
        tri = Delaunay(points)  # Compute the Delaunay triangulation of the vertices
        triangles = []  # Create a list of tuples representing the triangles in the triangulation
        for indices in tri.simplices:
            # triangles.append(tuple(indices))
            # print(indices)
            p1 = self.segment_list[indices[0]].get_start()
            p2 = self.segment_list[indices[1]].get_start()
            p3 = self.segment_list[indices[2]].get_start()
            triangle = Triangle(p1, p2, p3, '')
            triangles.append(triangle)
        return triangles

