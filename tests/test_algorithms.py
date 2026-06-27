"""Tests for geometry algorithms (no display required)."""
import unittest
import config
from Shapes.Point import Point
from Shapes.Segment import Segment
from Shapes.Polygon import Polygon
from app.algorithms import find_shape, _clear_overlay


def _make_square_polygon():
    """Return a unit-square Polygon with labelled points."""
    p1 = Point(0, 0, "A0")
    p2 = Point(1, 0, "B0")
    p3 = Point(1, 1, "C0")
    p4 = Point(0, 1, "D0")
    segs = [
        Segment(p1, p2, "s1"),
        Segment(p2, p3, "s2"),
        Segment(p3, p4, "s3"),
        Segment(p4, p1, "s4"),
    ]
    return Polygon(segs, "ABCD")


class TestFindShape(unittest.TestCase):
    def setUp(self):
        p = Point(1, 2, "A0")
        config.shapes = [p]

    def test_finds_existing(self):
        result = find_shape("A0")
        self.assertIsNotNone(result)
        self.assertEqual(result.get_label(), "A0")

    def test_returns_none_for_missing(self):
        self.assertIsNone(find_shape("Z99"))


class TestClearOverlay(unittest.TestCase):
    def setUp(self):
        config.null_segments = []
        config.shapes = []

    def test_removes_unlabelled_segments(self):
        p1, p2 = Point(0, 0, "A0"), Point(1, 1, "B0")
        labelled   = Segment(p1, p2, "S0")
        unlabelled = Segment(p1, p2, "")
        config.shapes = [labelled, unlabelled]
        _clear_overlay()
        self.assertIn(labelled, config.shapes)
        self.assertNotIn(unlabelled, config.shapes)

    def test_clears_null_segments_list(self):
        config.null_segments = ["something"]
        _clear_overlay()
        self.assertEqual(config.null_segments, [])


class TestPolygonArea(unittest.TestCase):
    def test_unit_square_area(self):
        poly = _make_square_polygon()
        self.assertAlmostEqual(poly.area(), 1.0)

    def test_rectangle_area(self):
        p1 = Point(0, 0, "A0")
        p2 = Point(4, 0, "B0")
        p3 = Point(4, 3, "C0")
        p4 = Point(0, 3, "D0")
        poly = Polygon([
            Segment(p1, p2, "s1"),
            Segment(p2, p3, "s2"),
            Segment(p3, p4, "s3"),
            Segment(p4, p1, "s4"),
        ], "RECT")
        self.assertAlmostEqual(poly.area(), 12.0)


class TestPolygonPerimeter(unittest.TestCase):
    def test_unit_square_perimeter(self):
        self.assertAlmostEqual(_make_square_polygon().perimeter(), 4.0)

    def test_3_4_5_triangle_perimeter(self):
        p1 = Point(0, 0, "A0")
        p2 = Point(3, 0, "B0")
        p3 = Point(0, 4, "C0")
        poly = Polygon([
            Segment(p1, p2, "s1"),
            Segment(p2, p3, "s2"),
            Segment(p3, p1, "s3"),
        ], "TRI")
        self.assertAlmostEqual(poly.perimeter(), 12.0)


class TestGrahamScan(unittest.TestCase):
    def test_square_hull_returns_segments(self):
        poly = _make_square_polygon()
        points = []
        for seg in poly.get_segment_list():
            for pt in (seg.get_start(), seg.get_end()):
                if pt not in points:
                    points.append(pt)
        hull = poly.graham_scan(points)
        # Hull must close the polygon: at least as many segments as vertices
        self.assertGreaterEqual(len(hull), len(points))
        # Every segment must be a Segment instance
        for seg in hull:
            self.assertIsInstance(seg, Segment)

    def test_fewer_than_3_points_returns_empty(self):
        poly = _make_square_polygon()
        hull = poly.graham_scan([Point(0, 0, "A0"), Point(1, 1, "B0")])
        self.assertEqual(hull, [])


class TestDelaunayTriangulation(unittest.TestCase):
    def test_square_triangulation_returns_triangles(self):
        poly = _make_square_polygon()
        triangles = poly.triangulation()
        self.assertGreater(len(triangles), 0)

    def test_triangles_have_3_vertices(self):
        poly = _make_square_polygon()
        for tri in poly.triangulation():
            self.assertIsNotNone(tri.get_p1())
            self.assertIsNotNone(tri.get_p2())
            self.assertIsNotNone(tri.get_p3())


if __name__ == "__main__":
    unittest.main()
