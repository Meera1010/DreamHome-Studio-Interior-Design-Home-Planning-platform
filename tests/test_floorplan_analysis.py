"""
DreamHome Studio — Floorplan Spatial Analysis Unit Tests
Tests room density checks, spatial collision detection, and layout rating scoring.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.floorplan_analysis_service import FloorplanAnalysisService

class TestFloorplanAnalysis(unittest.TestCase):
    """Unit test cases for FloorplanAnalysisService."""

    def test_room_analysis_good_layout(self):
        """Test analyzing a balanced room layout."""
        canvas_data = {
            "room": {"width_m": 8.0, "height_m": 6.0},
            "walls": [{"id": "w1"}],
            "openings": [{"type": "door"}, {"type": "window"}],
            "objects": [
                {"name": "Sofa", "x": 100, "y": 100, "width": 200, "depth": 90},
                {"name": "Table", "x": 400, "y": 400, "width": 100, "depth": 60}
            ]
        }
        res = FloorplanAnalysisService.analyze_room_layout(canvas_data)
        self.assertGreaterEqual(res["overall_score"], 80)
        self.assertEqual(res["metrics"]["door_count"], 1)
        self.assertEqual(res["metrics"]["window_count"], 1)

    def test_collision_detection(self):
        """Test detecting overlapping furniture items."""
        canvas_data = {
            "room": {"width_m": 5.0, "height_m": 5.0},
            "walls": [],
            "openings": [],
            "objects": [
                {"name": "Chair 1", "x": 100, "y": 100, "width": 100, "depth": 100},
                {"name": "Chair 2", "x": 150, "y": 150, "width": 100, "depth": 100}
            ]
        }
        res = FloorplanAnalysisService.analyze_room_layout(canvas_data)
        self.assertGreater(res["metrics"]["collisions_count"], 0)
        self.assertLess(res["overall_score"], 90)

if __name__ == "__main__":
    unittest.main()
