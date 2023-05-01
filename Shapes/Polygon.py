import numpy as np
from matplotlib.axes import Axes
from scipy.spatial import ConvexHull

import config
from Shapes.Line import Line
from Shapes.Point import Point
from Shapes.shapes import Shape


class Polygon(Shape):
    def __init__(self, lines_list, label):
        self.lines_list = lines_list
        self.label = label
        self.hidden = True

    def draw(self, ax: Axes):
        for line in self.lines_list:
            m, b = line.m_b()
            # draw_line_shape(m, b)
            x_range = np.array([-100, 1000])
            start = line.get_start()
            end = line.get_end()
            line.set_line_obj(ax.plot([start.get_x(), end.get_x()], [start.get_y(), end.get_y()], color='black', linestyle='-', linewidth=2))
            # line.dashes_obj, = ax.plot(x_range, m * x_range + b, linestyle='-', linewidth=1, color='black')

    def add_line(self, line):
        self.lines_list.append(line)

    def get_line_list(self):
        return self.lines_list

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
        x = [line.get_start().get_x() for line in self.lines_list] + [self.lines_list[-1].get_end().get_x()]
        y = [line.get_start().get_y() for line in self.lines_list] + [self.lines_list[-1].get_end().get_y()]
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
        for line in self.lines_list:
            perimeter += line.perimeter()
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
        for line in self.lines_list:
            start = line.get_start()
            end = line.get_end()
            points.append([start.get_x(), start.get_y()])
            points.append([end.get_x(), end.get_y()])
        hull = ConvexHull(points) # Calculate the convex hull of the points
        hull_lines = [] # Create a list of lines that form the convex hull
        for simplex in hull.simplices:
            start = simplex[0]
            end = simplex[1]
            x1, y1 = points[start]
            x2, y2 = points[end]
            hull_lines.append(Line(Point(x1, y1), Point(x2, y2)))
        return Polygon(hull_lines, self.label)
