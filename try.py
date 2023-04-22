import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class matplotlib_manager:
    def __init__(self):
        self.list_shape = []

    def add_shape(self, x, y, radius):
        circle = Circle((x, y), radius)
        self.list_shape.append(circle)

    def plot_all(self):
        fig, ax = plt.subplots()
        for shape in self.list_shape:
            ax.add_patch(shape)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.set_aspect('equal')
        plt.show()

l = matplotlib_manager()
l.add_circle(0, 1, 3)
l.plot_all()