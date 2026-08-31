"""
DreamHome Studio — Rendering Pipeline Unit Tests
Tests color space conversions (HEX, RGB, HSL), radial light falloff, and shadow ray wall occlusion.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.rendering_pipeline_service import RenderingPipelineService

class TestRenderingPipeline(unittest.TestCase):
    """Unit test cases for RenderingPipelineService."""

    def test_hex_to_rgb(self):
        """Test converting HEX string to RGB integer tuple."""
        rgb = RenderingPipelineService.hex_to_rgb("#1B4F72")
        self.assertEqual(rgb, (27, 79, 114))

    def test_rgb_to_hsl(self):
        """Test converting RGB integers to HSL tuple."""
        hsl = RenderingPipelineService.rgb_to_hsl(255, 0, 0) # Pure red
        self.assertEqual(hsl[0], 0.0) # 0 degrees hue
        self.assertEqual(hsl[1], 1.0) # 100% saturation

    def test_radial_light_falloff(self):
        """Test inverse-square distance light falloff math."""
        # At distance 0, falloff intensity should be 1.0
        val_center = RenderingPipelineService.calculate_radial_light_falloff(0, 0, 0, 0, 100, 1.0)
        self.assertEqual(val_center, 1.0)

        # Beyond radius, falloff should be 0.0
        val_outside = RenderingPipelineService.calculate_radial_light_falloff(0, 0, 150, 0, 100, 1.0)
        self.assertEqual(val_outside, 0.0)

    def test_trace_shadow_ray(self):
        """Test ray tracing wall occlusion check."""
        walls = [{"x1": 50, "y1": 0, "x2": 50, "y2": 100}] # Vertical wall at x=50
        
        # Ray from (0, 50) to (100, 50) crosses the wall -> Occluded
        is_occluded = RenderingPipelineService.trace_shadow_ray((0, 50), (100, 50), walls)
        self.assertTrue(is_occluded)

        # Ray from (0, 50) to (30, 50) does not cross the wall -> Not occluded
        is_clear = RenderingPipelineService.trace_shadow_ray((0, 50), (30, 50), walls)
        self.assertFalse(is_clear)

if __name__ == "__main__":
    unittest.main()
