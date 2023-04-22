
from Shapes.Circle import Circle2D
from Shapes.Line import Line2D
from Shapes.Point import Point2D
from Shapes.Rect import Rect2D
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


class matplotlib_manager:

    def __init__(self):
        self.list_shape = []
        #self.fig, self.ax = plt.subplots()

    def print_list(self):
        for obj in self.list_shape:
            print(obj)

    def add_shape(self, shape):
        self.list_shape.append(shape)

    def add_shapes(self, shapes_list):
        for shape in shapes_list:
            self.add_shape(shape)

    def plot_shape(self, shape, ax):
        if type(shape) is Circle2D:
            circle = plt.Circle((shape.get_x(), shape.get_y()), shape.get_radius(), edgecolor='black', fill=False)
            ax.add_patch(circle)

        # if type(shape) is Rect2D:
        #     ax.add_patch(Rectangle(shape., shape.get_y, shape.radius))

        return ax

    def plot_all(self):
        fig, ax = plt.subplots()
        for shape in self.list_shape:
            # ax.add_patch(shape)
            ax = self.plot_shape(shape, ax)

        ax.set_xlim(-2000, 2000)
        ax.set_ylim(-2000, 2000)
        plt.grid(True)

        ax.set_aspect('equal')
        plt.show()





if __name__ == '__main__':
    l = matplotlib_manager()
    i = [Circle2D(1, 2, 5),
         Circle2D(3, 2, 2)]
    l.add_shapes(i)
    l.print_list()
    #l.plot_all()


