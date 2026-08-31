"""
DreamHome Studio — Room Layout Generator Unit Tests
Tests automatic 2D room synthesis for living rooms, bedrooms, and dining spaces.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.room_layout_generator import RoomLayoutGeneratorService

class TestRoomLayoutGenerator(unittest.TestCase):
    """Unit test cases for RoomLayoutGeneratorService."""

    def test_living_room_generation(self):
        """Test synthesizing living room 2D canvas layout."""
        layout = RoomLayoutGeneratorService.generate_layout("Living Room Test", "Living Room", 8.0, 6.0)
        self.assertIn("room", layout)
        self.assertEqual(len(layout["walls"]), 4)
        self.assertGreater(len(layout["objects"]), 0)

    def test_bedroom_generation(self):
        """Test synthesizing bedroom 2D canvas layout."""
        layout = RoomLayoutGeneratorService.generate_layout("Master Suite", "Bedroom", 6.0, 5.0)
        self.assertEqual(layout["room"]["name"], "Master Suite")
        self.assertGreater(len(layout["objects"]), 0)

if __name__ == "__main__":
    unittest.main()
