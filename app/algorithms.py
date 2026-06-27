"""Geometry algorithms — convex hull, triangulation."""
from __future__ import annotations
import config
from Shapes.Segment import Segment
from Shapes.Polygon import Polygon


def find_shape(label: str):
    """Return the first shape whose label matches, or None."""
    for shape in config.shapes:
        if shape.get_label() == label:
            return shape
    return None


def run_convex_hull(polygon_label: str) -> str:
    """Compute and draw the convex hull of a polygon's vertices.

    Returns a comma-separated string of hull vertex labels.
    """
    _clear_overlay()
    polygon = find_shape(polygon_label)
    if polygon is None:
        return ""

    points: list = []
    for seg in polygon.get_segment_list():
        for pt in (seg.get_start(), seg.get_end()):
            if pt not in points:
                points.append(pt)

    hull_segments = polygon.graham_scan(points)
    seen_labels: list = []
    for seg in hull_segments:
        seg.draw(config.ax)
        config.null_segments.append(seg)
        lbl = seg.get_start().get_label()
        if lbl not in seen_labels:
            seen_labels.append(lbl)

    return ", ".join(seen_labels)


def run_triangulation(polygon_label: str) -> None:
    """Compute and draw the Delaunay triangulation of a polygon."""
    _clear_overlay()
    polygon = find_shape(polygon_label)
    if polygon is None:
        return
    for triangle in polygon.triangulation():
        triangle.draw(config.ax)
        config.null_segments.append(triangle)


def _clear_overlay() -> None:
    """Remove temporary overlay objects (unlabelled segments) from shapes."""
    config.null_segments = []
    config.shapes = [
        s for s in config.shapes
        if not (isinstance(s, Segment) and s.get_label() == "")
    ]
