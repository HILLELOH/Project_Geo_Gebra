# This is a sample Python script.
import Shapes
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Graphics import GUI_Graph
from Shapes.Point2D import Point2D


def print_hi():
    p = Point2D(3, 4, 0)
    q = Point2D(8, 5, 1)
    print(p.distance_from(q))

gg = GUI_Graph.Gui()

if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
