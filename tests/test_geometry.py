"""
DreamHome Studio — Geometry & 2D Math Unit Tests
Tests Shoelace polygon area, perimeter calculation, point distance, snap-to-grid,
and rotated bounding box geometry.
"""

import unittest
import math
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.geometry_service import GeometryService

class TestGeometryService(unittest.TestCase):
    """Test suite for 2D spatial geometry math service."""

    def test_shoelace_polygon_area(self):
        """Test polygon area calculation for rectangular room (8m x 6m = 48 sqm)."""
        vertices = [(0, 0), (8, 0), (8, 6), (0, 6)]
        area = GeometryService.calculate_polygon_area(vertices)
        self.assertEqual(area, 48.0)

    def test_polygon_perimeter(self):
        """Test perimeter calculation for 8m x 6m rectangle (28m)."""
        vertices = [(0, 0), (8, 0), (8, 6), (0, 6)]
        perimeter = GeometryService.calculate_perimeter(vertices)
        self.assertEqual(perimeter, 28.0)

    def test_point_distance(self):
        """Test Euclidean distance between (0,0) and (3,4)."""
        dist = GeometryService.point_distance((0, 0), (3, 4))
        self.assertEqual(dist, 5.0)

    def test_snap_to_grid(self):
        """Test coordinate alignment to 20px grid."""
        snapped = GeometryService.snap_to_grid(23.4, 38.9, 20.0)
        self.assertEqual(snapped, (20.0, 40.0))

    def test_rotate_point(self):
        """Test rotating (10, 0) by 90 degrees around (0,0)."""
        rotated = GeometryService.rotate_point((10, 0), (0, 0), 90)
        self.assertAlmostEqual(rotated[0], 0.0, places=3)
        self.assertAlmostEqual(rotated[1], 10.0, places=3)

    def test_line_intersection(self):
        """Test intersection between perpendicular line segments."""
        line1 = ((0, 5), (10, 5))
        line2 = ((5, 0), (5, 10))
        intersection = GeometryService.check_line_intersection(line1, line2)
        self.assertEqual(intersection, (5.0, 5.0))

if __name__ == "__main__":
    unittest.main()
