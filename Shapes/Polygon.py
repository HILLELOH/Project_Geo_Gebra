import numpy as np
from matplotlib.axes import Axes

import config
from Shapes.shapes import Shape


class Polygon(Shape):
    def __init__(self, segment_list, label):
        self.segment_list = segment_list
        self.label = label
        self.hidden = True

    def draw(self, ax: Axes):
        for segment in self.segment_list:
            # m, b = segment.m_b()
            # # draw_line_shape(m, b)
            # x_range = np.array([-100, 1000])
            start = segment.get_start()
            end = segment.get_end()
            segment.set_segment_obj(ax.plot([start.get_x(), end.get_x()], [start.get_y(), end.get_y()], color='black', linestyle='-', linewidth=2))
            # line.dashes_obj, = ax.plot(x_range, m * x_range + b, linestyle='-', linewidth=1, color='black')

    def add_segment(self, segment):
        self.segment_list.append(segment)

    def get_segment_list(self):
        return self.segment_list

    def get_label(self):
        return self.label

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, b):
        self.hidden = b
