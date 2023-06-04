import unittest
from Shapes.Point import *
from Shapes.Line import *
from Shapes.Segment import *
from Shapes.Circle import *
from Shapes.Polygon import *


class GeoGebra_TEST(unittest.TestCase):

    def test_points(self):
        p = Point(1, 2, "A")
        self.assertEqual(p.get_x(), 1)
        self.assertEqual(p.get_y(), 2)
        self.assertEqual(p.get_label(), "A")
        self.assertEqual(p.is_hidden(), False)

        self.assertEqual(p.area(), 0)
        self.assertEqual(p.perimeter(), 0)
        self.assertEqual(p.convex_hull(), p)

    def test_lines(self):
        p1 = Point(0, 0, "A")
        p2 = Point(5, 0, "B")
        l = Line(p1, p2, "AB")
        self.assertEqual(l.get_start(), p1)
        self.assertEqual(l.get_end(), p2)
        self.assertEqual(l.get_label(), "AB")
        self.assertEqual(l.is_hidden(), False)

        self.assertEqual(l.area(), 0)
        self.assertEqual(l.perimeter(), 5)
        self.assertEqual(l.convex_hull(), l)

    def test_segments(self):
        p1 = Point(0, 2, "A")
        p2 = Point(0, 0, "B")
        s = Segment(p1, p2, "AB")
        self.assertEqual(s.get_start(), p1)
        self.assertEqual(s.get_end(), p2)
        self.assertEqual(s.get_label(), "AB")
        self.assertEqual(s.is_hidden(), False)

        self.assertEqual(s.area(), 0)
        self.assertEqual(s.perimeter(), 2)
        self.assertEqual(s.convex_hull(), s)

    def test_circles(self):
        p = Point(1, 2, "A")
        c = Circle(p, 3, "C")
        self.assertEqual(c.get_center(), p)
        self.assertEqual(c.get_radius(), 3)
        self.assertEqual(c.get_label(), "C")
        self.assertEqual(c.is_hidden(), False)

        self.assertEqual(c.area(), math.pi*3**2)
        self.assertEqual(c.perimeter(), 2*math.pi*3)

    def test_polygons(self):
        p1 = Point(-4, 0, "A")
        p2 = Point(4, 0, "B")
        p3 = Point(4, 4, "C")
        p4 = Point(-4, 4, "D")

        seg1 = Segment(p1, p2, "AB")
        seg2 = Segment(p2, p3, "BC")
        seg3 = Segment(p3, p4, "CD")
        seg4 = Segment(p4, p1, "DA")

        self.assertEqual(seg1.perimeter(), 8)
        self.assertEqual(seg2.perimeter(), 4)
        self.assertEqual(seg3.perimeter(), 8)
        self.assertEqual(seg4.perimeter(), 4)

        poly = Polygon([seg1, seg2, seg3, seg4], "ABCD")

        self.assertEqual(poly.get_segment_list(), [seg1, seg2, seg3, seg4])

        self.assertEqual(poly.get_label(), "ABCD")
        self.assertEqual(poly.is_hidden(), True)
        self.assertEqual(poly.area(), 8*4)
        self.assertEqual(poly.perimeter(), 8+8+4+4)
        # self.assertEqual(poly.convex_hull(), poly)

if __name__ == '__main__':
    unittest.main()