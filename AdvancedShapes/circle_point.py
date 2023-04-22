import Shapes as normal_shape

class point_circle:
    point = normal_shape.Point
    circle = normal_shape.Circle
    def __init__(self, id, pc_x, pc_y, radius):
        self._id = id
        self._pc_x = pc_x
        self._pc_y = pc_y
        self._radius = radius


    def getID(self):
        return self._id

    def getPc_x(self):
        return self._pc_x

    def setPc_x(self, newX):
        self._pc_x = newX

    def getPc_y(self):
        return self._pc_y

    def setPc_y(self, newY):
        self._pc_y = newY

    def getRadius(self):
        return self._radius

    def setRadius(self, newRadius):
        self._radius = newRadius
