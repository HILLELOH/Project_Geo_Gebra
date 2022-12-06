import Shapes as normal_shape

class point_circle:
    point = normal_shape.Point2D
    circle = normal_shape.Circle2D
    def __init__(self,id, pc_x, pc_y, radius):
        self._id = id
        self._pc_x = pc_x
        self._pc_y = pc_y
        self._radius = radius


     #getters
    def getID(self):
        return self._id

    def getPc_x(self):
        return self._pc_x

    def getPc_y(self):
        return self._pc_y

    def getRadius(self):
        return self._radius


    #setter (we dont want to have access to change id)
    def setPc_x(self, newX):
        self._pc_x = newX

    def setPc_y(self, newY):
        self._pc_y = newY

    def setRadius(self, newRadius):
        self._radius = newRadius
