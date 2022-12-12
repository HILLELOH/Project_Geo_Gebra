from Shapes.ICircle2D import ICircle2D


class Circle2D(ICircle2D):
    def __init__(self, _id, x, y, radius):
        self._id = _id
        self.x = x
        self.y = y
        self.radius = radius

    def get_id(self):
        return self._id

    def get_x(self):
        return self.x

    def set_x(self, new_x):
        self.x = new_x

    def get_y(self):
        return self.y

    def set_y(self, new_y):
        self.y = new_y

    def get_radius(self):
        return self.radius

    def set_radius(self, new_radius):
        self.radius = new_radius




