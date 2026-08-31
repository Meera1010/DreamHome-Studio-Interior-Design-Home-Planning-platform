# DreamHome Studio — Testing Guide

## Running Automated Tests

Run the complete test suite:

```bash
python tests/run_tests.py
```

### Test Suite Structure

* `tests/test_auth.py`: Tests password hashing, login, roles, user updates.
* `tests/test_projects.py`: Tests project creation, client-designer links, status filters.
* `tests/test_floorplans.py`: Tests 2D room layouts, version history, SVG export.
* `tests/test_geometry.py`: Tests Shoelace polygon area, perimeter, snapping, point rotation.
* `tests/test_budget.py`: Tests cost calculator engine, taxes, margins, CSV export.
* `tests/test_collaboration.py`: Tests feedback pin comments and approval requests.
* `tests/test_api_endpoints.py`: End-to-end integration tests for REST API.
* `tests/test_admin.py`: Tests admin user management and audit logs.
