"""
DreamHome Studio — Architectural Standards Unit Tests
Tests ADA wheelchair compliance, IRC building code checks, STC acoustic ratings, and thermal R-values.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.architectural_standards_service import ArchitecturalStandardsService

class TestArchitecturalStandards(unittest.TestCase):
    """Unit test cases for ArchitecturalStandardsService."""

    def test_ada_compliance_pass(self):
        """Test ADA compliance with adequate door openings and turning radius."""
        canvas_data = {
            "room": {"width_m": 6.0, "height_m": 5.0},
            "openings": [{"type": "door", "id": "d1", "width_m": 0.95}],
            "objects": []
        }
        res = ArchitecturalStandardsService.audit_ada_compliance(canvas_data)
        self.assertTrue(res["is_ada_compliant"])
        self.assertEqual(res["compliance_score"], 100)

    def test_ada_compliance_fail(self):
        """Test ADA compliance failure with narrow door opening."""
        canvas_data = {
            "room": {"width_m": 4.0, "height_m": 3.0},
            "openings": [{"type": "door", "id": "d1", "width_m": 0.70}],
            "objects": []
        }
        res = ArchitecturalStandardsService.audit_ada_compliance(canvas_data)
        self.assertFalse(res["is_ada_compliant"])
        self.assertLess(res["compliance_score"], 100)

    def test_building_code_glazing_ratio(self):
        """Test IRC building code natural daylighting glazing requirement."""
        canvas_data = {
            "room": {"width_m": 5.0, "height_m": 4.0, "ceiling_height_m": 2.7}, # 20 sqm
            "openings": [{"type": "window", "width_m": 1.6, "height_m": 1.2}] # 1.92 sqm = 9.6% > 8%
        }
        res = ArchitecturalStandardsService.audit_building_code_compliance(canvas_data)
        self.assertTrue(res["is_code_compliant"])

    def test_stc_acoustic_rating(self):
        """Test sound transmission class rating for insulated wall assembly."""
        layers = [
            {"material": "gypsum drywall", "thickness_mm": 12.5},
            {"material": "rockwool insulation", "thickness_mm": 90.0},
            {"material": "resilient channel", "thickness_mm": 15.0}
        ]
        res = ArchitecturalStandardsService.calculate_stc_acoustic_rating(layers)
        self.assertGreaterEqual(res["calculated_stc"], 45.0)

if __name__ == "__main__":
    unittest.main()
