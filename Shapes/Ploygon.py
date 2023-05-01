import numpy as np
from matplotlib.axes import Axes

import config
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
