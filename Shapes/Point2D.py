from math import sqrt

from Shapes.IPoint2D import IPoint2D


class Point2D(IPoint2D):
    def __init__(self, _id, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._id = id

    def set_location(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_id(self):
        return self._id

    def get_x(self):
        return self.pos_x

    def set_x(self, new_x):
        self.pos_x = new_x

    def get_y(self):
        return self.pos_y

    def set_y(self, new_y):
        self.pos_y = new_y

    def move_point(self, new_x, new_y):
        self.pos_x = new_x
        self.pos_y = new_y

    def distance_from(self, from_p):
        return sqrt(pow((self.get_x() - from_p.get_x()), 2) + pow((self.get_y() - from_p.get_y()), 2))
