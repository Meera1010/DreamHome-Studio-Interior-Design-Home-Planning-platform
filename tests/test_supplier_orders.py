"""
DreamHome Studio — Supplier Order & Inventory Service Unit Tests
Tests low stock inventory audit and formal purchase order generation.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import get_db
from backend.models.supplier import Supplier
from backend.models.inventory import InventoryItem
from backend.services.supplier_order_service import SupplierOrderService

class TestSupplierOrders(unittest.TestCase):
    """Unit test cases for SupplierOrderService."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM inventory_items;")
        self.db.execute("DELETE FROM furniture_catalog;")
        self.db.execute("DELETE FROM suppliers;")
        self.db.execute("DELETE FROM sqlite_sequence WHERE name IN ('suppliers', 'inventory_items', 'furniture_catalog');")
        self.db.execute("INSERT INTO furniture_catalog (id, name, category, subcategory, sku, brand, width_cm, depth_cm, height_cm, price, color_options_json, material) VALUES (1, 'Test Sofa', 'Living', 'Sofas', 'SKU-TEST-001', 'Test', 200.0, 90.0, 80.0, 100.0, '[\"#FFFFFF\"]', 'Fabric');")
        self.supplier = Supplier.create(**{"company_name": "Milano Living", "contact_name": "Milano Sales", "email": "contact@milano.it", "phone": "+39-02-5551234", "address": "Milan, Italy", "lead_time_days": 14, "rating": 4.8})
        self.item = InventoryItem.create(**{"furniture_id": 1, "supplier_id": self.supplier.id, "quantity_in_stock": 2, "reorder_level": 5, "unit_cost": 1200.00, "bin_location": "A-12", "status": "In Stock"})

    def test_low_stock_audit(self):
        """Test identifying inventory items requiring reordering."""
        low_stock = SupplierOrderService.audit_low_stock_items()
        self.assertGreater(len(low_stock), 0)
        self.assertEqual(low_stock[0]["sku"], "SKU-TEST-001")

    def test_purchase_order_generation(self):
        """Test generating purchase order payload."""
        orders = [{"inventory_id": self.item.id, "furniture_name": "Leather Sofa", "sku": "SKU-S1", "quantity": 10, "unit_cost": 1200.00}]
        po = SupplierOrderService.generate_purchase_order(self.supplier.id, orders)
        self.assertIn("po_number", po)
        self.assertEqual(po["total_order_cost"], 12000.00)

if __name__ == "__main__":
    unittest.main()
