"""
DreamHome Studio — Master Automated Test Suite Runner
Discovers and executes all unit and integration test modules across the application.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Import all test cases
from tests.test_auth import TestAuthSecurity
from tests.test_projects import TestProjects
from tests.test_floorplans import TestFloorplans
from tests.test_geometry import TestGeometryService
from tests.test_budget import TestBudgetEngine
from tests.test_collaboration import TestCollaboration
from tests.test_api_endpoints import TestAPIEndpoints
from tests.test_admin import TestAdminAudit
from tests.test_extended_catalog import TestExtendedCatalog
from tests.test_floorplan_analysis import TestFloorplanAnalysis
from tests.test_supplier_orders import TestSupplierOrders
from tests.test_layout_generator import TestRoomLayoutGenerator
from tests.test_lighting_service import TestLightingService
from tests.test_architectural_standards import TestArchitecturalStandards
from tests.test_rendering_pipeline import TestRenderingPipeline

def build_test_suite() -> unittest.TestSuite:
    """Construct complete master test suite."""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestAuthSecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestProjects))
    suite.addTests(loader.loadTestsFromTestCase(TestFloorplans))
    suite.addTests(loader.loadTestsFromTestCase(TestGeometryService))
    suite.addTests(loader.loadTestsFromTestCase(TestBudgetEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCollaboration))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestAdminAudit))
    suite.addTests(loader.loadTestsFromTestCase(TestExtendedCatalog))
    suite.addTests(loader.loadTestsFromTestCase(TestFloorplanAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestSupplierOrders))
    suite.addTests(loader.loadTestsFromTestCase(TestRoomLayoutGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestLightingService))
    suite.addTests(loader.loadTestsFromTestCase(TestArchitecturalStandards))
    suite.addTests(loader.loadTestsFromTestCase(TestRenderingPipeline))

    return suite

def main():
    print("=" * 80)
    print("               DREAMHOME STUDIO — AUTOMATED TEST SUITE RUNNER            ")
    print("=" * 80)

    suite = build_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 80)
    if result.wasSuccessful():
        print(f"[OK] SUCCESS: All {result.testsRun} automated test cases passed clean!")
        sys.exit(0)
    else:
        print(f"[FAIL] FAILURE: {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()
