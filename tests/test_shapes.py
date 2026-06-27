"""Tests for geometry primitive classes."""
import math
import unittest

from Shapes.Point import Point
from Shapes.Line import Line
from Shapes.Segment import Segment
from Shapes.Circle import Circle
from Shapes.Polygon import Polygon


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.p = Point(3.0, 4.0, "A0")

    def test_coordinates(self):
        self.assertEqual(self.p.get_x(), 3.0)
        self.assertEqual(self.p.get_y(), 4.0)

    def test_label(self):
        self.assertEqual(self.p.get_label(), "A0")

    def test_hidden_default_false(self):
        self.assertFalse(self.p.is_hidden())

    def test_set_hidden(self):
        self.p.set_hidden(True)
        self.assertTrue(self.p.is_hidden())
        self.p.set_hidden(False)
        self.assertFalse(self.p.is_hidden())

    def test_set_x_delta(self):
        self.p.set_x(2.0)
        self.assertAlmostEqual(self.p.get_x(), 5.0)

    def test_set_y_delta(self):
        self.p.set_y(-1.0)
        self.assertAlmostEqual(self.p.get_y(), 3.0)

    def test_set_p_absolute(self):
        self.p.set_p(10.0, 20.0)
        self.assertEqual(self.p.get_x(), 10.0)
        self.assertEqual(self.p.get_y(), 20.0)

    def test_area_is_zero(self):
        self.assertEqual(self.p.area(), 0)

    def test_perimeter_is_zero(self):
        self.assertEqual(self.p.perimeter(), 0)

    def test_repr(self):
        self.assertIn("3.000", repr(self.p))
        self.assertIn("4.000", repr(self.p))

    def test_is_line_part_false_when_no_shapes(self):
        self.assertFalse(self.p.is_line_part([]))

    def test_is_circle_part_false_when_no_shapes(self):
        self.assertFalse(self.p.is_circle_part([]))

    def test_is_segment_part_false_when_no_shapes(self):
        self.assertFalse(self.p.is_segment_part([]))

    def test_is_polygon_part_false_when_no_shapes(self):
        self.assertFalse(self.p.is_polygon_part([]))

    def test_is_line_part_returns_line(self):
        p1 = Point(0, 0, "A0")
        p2 = Point(1, 1, "B0")
        line = Line(p1, p2, "L0")
        self.assertEqual(p1.is_line_part([p1, p2, line]), line)
        self.assertEqual(p2.is_line_part([p1, p2, line]), line)

    def test_is_segment_part_returns_segment(self):
        p1 = Point(0, 0, "A0")
        p2 = Point(1, 1, "B0")
        seg = Segment(p1, p2, "S0")
        self.assertEqual(p1.is_segment_part([p1, p2, seg]), seg)

    def test_is_circle_part_returns_circle(self):
        center = Point(0, 0, "A0")
        circle = Circle(center, 5.0, "C0")
        self.assertEqual(center.is_circle_part([center, circle]), circle)

    def test_is_in_poly(self):
        p1 = Point(0, 0, "A0")
        p2 = Point(1, 0, "B0")
        p3 = Point(1, 1, "C0")
        p4 = Point(0, 1, "D0")
        s1 = Segment(p1, p2, "s1")
        s2 = Segment(p2, p3, "s2")
        s3 = Segment(p3, p4, "s3")
        s4 = Segment(p4, p1, "s4")
        poly = Polygon([s1, s2, s3, s4], "ABCD")
        self.assertTrue(p1.is_in_poly(poly))
        outside = Point(5, 5, "X0")
        self.assertFalse(outside.is_in_poly(poly))


class TestLine(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(0.0, 0.0, "A0")
        self.p2 = Point(3.0, 4.0, "B0")
        self.line = Line(self.p1, self.p2, "L0")

    def test_endpoints(self):
        self.assertIs(self.line.get_start(), self.p1)
        self.assertIs(self.line.get_end(), self.p2)

    def test_label(self):
        self.assertEqual(self.line.get_label(), "L0")

    def test_hidden_default_false(self):
        self.assertFalse(self.line.is_hidden())

    def test_set_hidden(self):
        self.line.set_hidden(True)
        self.assertTrue(self.line.is_hidden())

    def test_perimeter_is_euclidean_distance(self):
        self.assertAlmostEqual(self.line.perimeter(), 5.0)

    def test_area_is_zero(self):
        self.assertEqual(self.line.area(), 0)

    def test_m_b_diagonal(self):
        m, b = self.line.m_b()
        self.assertAlmostEqual(m, 4 / 3)
        self.assertAlmostEqual(b, 0.0)

    def test_m_b_horizontal(self):
        line = Line(Point(0, 2, "A0"), Point(5, 2, "B0"), "L0")
        m, b = line.m_b()
        self.assertIsNone(b)        # horizontal: (y, None)
        self.assertAlmostEqual(m, 2.0)

    def test_m_b_vertical(self):
        line = Line(Point(3, 0, "A0"), Point(3, 5, "B0"), "L0")
        m, b = line.m_b()
        self.assertIsNone(m)        # vertical: (None, x)
        self.assertAlmostEqual(b, 3.0)

    def test_set_start_end_point(self):
        self.line.set_start_point(1.0, 1.0)
        self.assertAlmostEqual(self.p1.get_x(), 1.0)
        self.assertAlmostEqual(self.p1.get_y(), 1.0)
        self.line.set_end_point(-1.0, -1.0)
        self.assertAlmostEqual(self.p2.get_x(), 2.0)
        self.assertAlmostEqual(self.p2.get_y(), 3.0)


class TestSegment(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(0.0, 0.0, "A0")
        self.p2 = Point(0.0, 5.0, "B0")
        self.seg = Segment(self.p1, self.p2, "S0")

    def test_endpoints(self):
        self.assertIs(self.seg.get_start(), self.p1)
        self.assertIs(self.seg.get_end(), self.p2)

    def test_label(self):
        self.assertEqual(self.seg.get_label(), "S0")

    def test_hidden_default_false(self):
        self.assertFalse(self.seg.is_hidden())

    def test_perimeter_vertical(self):
        self.assertAlmostEqual(self.seg.perimeter(), 5.0)

    def test_perimeter_diagonal(self):
        seg = Segment(Point(0, 0, "A0"), Point(3, 4, "B0"), "S0")
        self.assertAlmostEqual(seg.perimeter(), 5.0)

    def test_area_is_zero(self):
        self.assertEqual(self.seg.area(), 0)

    def test_m_b_vertical(self):
        m, b = self.seg.m_b()
        self.assertIsNone(m)
        self.assertAlmostEqual(b, 0.0)

    def test_m_b_horizontal(self):
        seg = Segment(Point(0, 3, "A0"), Point(5, 3, "B0"), "S0")
        m, b = seg.m_b()
        self.assertIsNone(b)
        self.assertAlmostEqual(m, 3.0)


class TestCircle(unittest.TestCase):
    def setUp(self):
        self.center = Point(1.0, 2.0, "O0")
        self.circle = Circle(self.center, 3.0, "C0")

    def test_center(self):
        self.assertIs(self.circle.get_center(), self.center)

    def test_radius(self):
        self.assertAlmostEqual(self.circle.get_radius(), 3.0)

    def test_label(self):
        self.assertEqual(self.circle.get_label(), "C0")

    def test_hidden_default_false(self):
        self.assertFalse(self.circle.is_hidden())

    def test_area(self):
        self.assertAlmostEqual(self.circle.area(), math.pi * 9)

    def test_perimeter(self):
        self.assertAlmostEqual(self.circle.perimeter(), 2 * math.pi * 3)

    def test_set_hidden(self):
        self.circle.set_hidden(True)
        self.assertTrue(self.circle.is_hidden())

    def test_set_center_delta(self):
        self.circle.set_center(2.0, -1.0)
        self.assertAlmostEqual(self.center.get_x(), 3.0)
        self.assertAlmostEqual(self.center.get_y(), 1.0)


class TestPolygon(unittest.TestCase):
    def setUp(self):
        # Unit square: (0,0) (1,0) (1,1) (0,1)
        p1 = Point(0, 0, "A0")
        p2 = Point(1, 0, "B0")
        p3 = Point(1, 1, "C0")
        p4 = Point(0, 1, "D0")
        self.s1 = Segment(p1, p2, "s1")
        self.s2 = Segment(p2, p3, "s2")
        self.s3 = Segment(p3, p4, "s3")
        self.s4 = Segment(p4, p1, "s4")
        self.poly = Polygon([self.s1, self.s2, self.s3, self.s4], "ABCD")

    def test_segment_list(self):
        self.assertEqual(
            self.poly.get_segment_list(),
            [self.s1, self.s2, self.s3, self.s4],
        )

    def test_label(self):
        self.assertEqual(self.poly.get_label(), "ABCD")

    def test_hidden_default_true(self):
        self.assertTrue(self.poly.is_hidden())

    def test_area_unit_square(self):
        self.assertAlmostEqual(self.poly.area(), 1.0)

    def test_perimeter_unit_square(self):
        self.assertAlmostEqual(self.poly.perimeter(), 4.0)

    def test_area_rectangle(self):
        p1 = Point(-4, 0, "A0")
        p2 = Point(4, 0, "B0")
        p3 = Point(4, 4, "C0")
        p4 = Point(-4, 4, "D0")
        poly = Polygon([
            Segment(p1, p2, "s1"),
            Segment(p2, p3, "s2"),
            Segment(p3, p4, "s3"),
            Segment(p4, p1, "s4"),
        ], "RECT")
        self.assertAlmostEqual(poly.area(), 32.0)

    def test_set_label_appends(self):
        poly = Polygon([], "")
        poly.set_label("A0")
        self.assertEqual(poly.get_label(), "A0")
        poly.set_label("B0")
        self.assertEqual(poly.get_label(), "A0, B0")

    def test_add_segment(self):
        extra = Segment(Point(0, 0, "X0"), Point(1, 1, "Y0"), "e1")
        initial_count = len(self.poly.get_segment_list())
        self.poly.add_segment(extra)
        self.assertEqual(len(self.poly.get_segment_list()), initial_count + 1)


if __name__ == "__main__":
    unittest.main()
