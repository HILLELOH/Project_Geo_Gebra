from math import sqrt

from Shapes.ILine2D import ILine2D


class Line2D(ILine2D):
    def __init__(self, _id, a_x, a_y, b_x, b_y):
        self._id = _id
        self.a_x = a_x
        self.a_y = a_y
        self.b_x = b_x
        self.b_y = b_y

    def get_id(self):
        return self._id

    def get_a_x(self):
        return self.a_x

    def set_a_x(self, new_x):
        self.a_x = new_x

    def get_a_y(self):
        return self.a_y

    def set_a_y(self, new_y):
        self.a_y = new_y

    def get_b_x(self):
        return self.a_x

    def set_b_x(self, new_x):
        self.b_x = new_x

    def get_b_y(self):
        return self.a_x

    def set_b_y(self, new_y):
        self.b_y = new_y

    def len(self, l):
        return sqrt(pow((l.get_a_x() - l.get_b_x), 2)+pow((l.get_a_y() - l.get_b_y), 2))
