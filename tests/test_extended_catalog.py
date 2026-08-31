"""
DreamHome Studio — Extended Catalog Service Unit Tests
Tests multi-attribute filtering, price range grouping, dimension spatial bounds, and catalog facets.
"""

import os
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import DatabaseManager, get_db
from backend.models.furniture import FurnitureCatalog
from backend.services.extended_catalog_service import ExtendedCatalogService

class TestExtendedCatalog(unittest.TestCase):
    """Unit test cases for ExtendedCatalogService."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM budget_line_items;")
        self.db.execute("DELETE FROM inventory_items;")
        self.db.execute("DELETE FROM furniture_catalog;")
        self.db.execute("DELETE FROM sqlite_sequence WHERE name IN ('furniture_catalog', 'inventory_items', 'budget_line_items');")
        # Insert sample furniture items
        FurnitureCatalog.create(**{"name": "Nordic Leather Sofa", "category": "Living Room", "subcategory": "Sofas", "sku": "SKU-S1", "brand": "Nordic", "width_cm": 220.0, "depth_cm": 95.0, "height_cm": 85.0, "price": 1850.00, "color_options_json": '["#1C2833"]', "material": "Leather"})
        FurnitureCatalog.create(**{"name": "Marble Coffee Table", "category": "Living Room", "subcategory": "Tables", "sku": "SKU-T1", "brand": "Milano", "width_cm": 110.0, "depth_cm": 110.0, "height_cm": 45.0, "price": 950.00, "color_options_json": '["#FFFFFF"]', "material": "Marble"})
        FurnitureCatalog.create(**{"name": "Solid Oak Bed", "category": "Bedroom", "subcategory": "Beds", "sku": "SKU-B1", "brand": "Nordic", "width_cm": 210.0, "depth_cm": 180.0, "height_cm": 120.0, "price": 2200.00, "color_options_json": '["#F5CBA7"]', "material": "Oak"})

    def test_search_by_category(self):
        """Test searching furniture by category."""
        res = ExtendedCatalogService.search_furniture_advanced(category="Living Room")
        self.assertEqual(res["total_items"], 2)

    def test_search_by_price_range(self):
        """Test searching furniture within a price range."""
        res = ExtendedCatalogService.search_furniture_advanced(min_price=1000.0, max_price=2000.0)
        self.assertEqual(res["total_items"], 1)
        self.assertEqual(res["items"][0]["name"], "Nordic Leather Sofa")

    def test_catalog_facets(self):
        """Test retrieving category and price stats facets."""
        facets = ExtendedCatalogService.get_catalog_facets()
        self.assertIn("categories", facets)
        self.assertIn("price_stats", facets)
        self.assertEqual(facets["price_stats"]["min_price"], 950.0)
        self.assertEqual(facets["price_stats"]["max_price"], 2200.0)

if __name__ == "__main__":
    unittest.main()
