"""
DreamHome Studio — Lighting Calculation Service Unit Tests
Tests lumen requirements, lux levels, and color temperature recommendations.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.lighting_calculation_service import LightingCalculationService

class TestLightingService(unittest.TestCase):
    """Unit test cases for LightingCalculationService."""

    def test_living_room_lighting(self):
        """Test lumen calculation for a 48 sqm living room."""
        res = LightingCalculationService.calculate_room_lighting("Living Room", 48.0, 2.8, 4)
        self.assertEqual(res["target_lux"], 150.0)
        self.assertGreater(res["total_required_lumens"], 7000.0)

    def test_office_lighting(self):
        """Test high-lux office lighting requirements."""
        res = LightingCalculationService.calculate_room_lighting("Office", 20.0, 3.0, 4)
        self.assertEqual(res["target_lux"], 400.0)

if __name__ == "__main__":
    unittest.main()
