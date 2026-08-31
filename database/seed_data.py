"""
DreamHome Studio — Database Seed Generator
Seeds database with realistic, production-ready sample data for users, catalog items,
materials, suppliers, projects, 2D canvas floorplans, budgets, tasks, moodboards,
comments, approvals, portfolios, notifications, and audit logs.
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.db_manager import get_db

def hash_password(password: str) -> str:
    """Hash password using PBKDF2 with SHA-256 for secure seed storage."""
    salt = "dh_studio_salt_983741"
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

def seed_database(db_path: str = None) -> None:
    """Populate database with comprehensive realistic seed datasets."""
    db = get_db(db_path)
    db.init_db()

    print("Seeding database...")

    # Clear existing data in reverse order of foreign keys
    tables = [
        "audit_logs", "notifications", "portfolios", "approval_requests",
        "comments", "moodboards", "tasks", "budget_line_items", "budgets",
        "inventory_items", "suppliers", "materials_catalog",
        "floorplan_versions", "floorplans", "furniture_catalog", "projects", "users"
    ]
    for table in tables:
        db.execute(f"DELETE FROM {table};")
        db.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

    # 1. Users
    pwd_admin = hash_password("Admin123!Password")
    pwd_designer = hash_password("Designer123!Password")
    pwd_client = hash_password("Client123!Password")

    users_data = [
        ("admin@dreamhome.com", pwd_admin, "System Administrator", "Admin", "/static/images/avatars/admin.jpg", "+1-800-555-0100", "DreamHome HQ", "Chief System Admin & Lead Architect"),
        ("sarah.jenkins@dreamhome.com", pwd_designer, "Sarah Jenkins", "Designer", "/static/images/avatars/sarah.jpg", "+1-555-0192", "Studio Jenkins", "Senior Interior Architect & Lighting Specialist"),
        ("alex.rivera@dreamhome.com", pwd_designer, "Alex Rivera", "Designer", "/static/images/avatars/alex.jpg", "+1-555-0184", "Rivera Design Co", "Modern Minimalist & Space Planner"),
        ("john.doe@gmail.com", pwd_client, "John Doe", "Client", "/static/images/avatars/john.jpg", "+1-555-0171", "Acme Enterprises", "Homeowner - Modern Villa Project"),
        ("emma.watson@gmail.com", pwd_client, "Emma Watson", "Client", "/static/images/avatars/emma.jpg", "+1-555-0163", "Watson Media", "Client - Scandinavian Loft Project"),
        ("michael.brown@gmail.com", pwd_client, "Michael Brown", "Client", "/static/images/avatars/michael.jpg", "+1-555-0155", "Apex Capital", "Client - Luxury Office Project")
    ]

    for u in users_data:
        db.execute(
            "INSERT INTO users (email, password_hash, full_name, role, avatar_url, phone, company, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            u
        )

    # 2. Suppliers
    suppliers_data = [
        ("Nordic Design Co.", "Hens Lindqvist", "contact@nordicdesign.com", "+46-8-123456", "https://nordicdesign.example.com", "Stockholm, Sweden", 4.9, 12, "Premium Scandinavian hardwood furniture & textiles"),
        ("Milano Luxury Living", "Gianna Rossi", "sales@milanoluxury.it", "+39-02-987654", "https://milanoluxury.example.com", "Milan, Italy", 4.8, 21, "Italian leather sofas, marble dining tables & chandeliers"),
        ("Artisan Craftsman Ltd", "David Miller", "orders@artisancrafts.com", "+1-415-555-8899", "https://artisancrafts.example.com", "San Francisco, USA", 4.7, 7, "Handcrafted solid oak tables, custom cabinets & brass fixtures"),
        ("Zenith Lighting Labs", "Elena Rostova", "support@zenithlighting.com", "+44-20-79460912", "https://zenithlighting.example.com", "London, UK", 4.95, 5, "Architectural LED fixtures, ambient lamps & smart lighting"),
        ("EcoTile & Surface Tech", "Carlos Gomez", "info@ecotile.es", "+34-91-334455", "https://ecotile.example.com", "Valencia, Spain", 4.6, 14, "Recycled ceramic tiles, terrazzo & natural stone slabs")
    ]

    for s in suppliers_data:
        db.execute(
            "INSERT INTO suppliers (company_name, contact_name, email, phone, website, address, rating, lead_time_days, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            s
        )

    # 3. Furniture Catalog
    from database.catalog_items_bedroom import BEDROOM_CATALOG_DATA
    from database.catalog_items_living import LIVING_CATALOG_DATA
    from database.catalog_items_dining import DINING_CATALOG_DATA
    from database.catalog_items_office import OFFICE_CATALOG_DATA
    from database.catalog_items_lighting import LIGHTING_CATALOG_DATA
    from database.catalog_items_decor import DECOR_CATALOG_DATA
    from database.catalog_items_bathroom import BATHROOM_CATALOG_DATA
    from database.catalog_items_kitchen import KITCHEN_CATALOG_DATA
    from database.seed_furniture_catalog import FURNITURE_SEED_DATA
    from database.seed_materials_catalog import MATERIALS_SEED_DATA

    furniture_data = (
        FURNITURE_SEED_DATA + BEDROOM_CATALOG_DATA + LIVING_CATALOG_DATA +
        DINING_CATALOG_DATA + OFFICE_CATALOG_DATA + LIGHTING_CATALOG_DATA +
        DECOR_CATALOG_DATA + BATHROOM_CATALOG_DATA + KITCHEN_CATALOG_DATA
    )

    seen_skus = set()
    for idx, f in enumerate(furniture_data, start=1):
        f_list = list(f)
        sku = f_list[3]
        if sku in seen_skus:
            sku = f"{sku}-{idx}"
            f_list[3] = sku
        seen_skus.add(sku)

        db.execute(
            """INSERT INTO furniture_catalog 
               (name, category, subcategory, sku, brand, width_cm, depth_cm, height_cm, price, color_options_json, material, texture_url, thumbnail_url, default_z_index, is_customizable) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(f_list)
        )

    # 4. Materials Catalog
    for m in MATERIALS_SEED_DATA:
        db.execute(
            """INSERT INTO materials_catalog 
               (name, category, texture_url, pattern_type, color_hex, price_per_sqm, roughness, opacity) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            m
        )

    # 5. Inventory Items
    # Link furniture to suppliers
    num_furniture = len(furniture_data)
    num_suppliers = len(suppliers_data)
    for furniture_id in range(1, num_furniture + 1):
        supplier_id = ((furniture_id - 1) % num_suppliers) + 1
        stock_qty = 12 + (furniture_id * 3)
        unit_cost = 100.00 + (furniture_id * 45.00)
        db.execute(
            """INSERT INTO inventory_items 
               (furniture_id, supplier_id, quantity_in_stock, reorder_level, unit_cost, bin_location, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (furniture_id, supplier_id, stock_qty, 5, unit_cost, f"BIN-A{furniture_id:02d}", "In Stock")
        )

    # 6. Projects
    projects_data = [
        ("Modern Coastal Villa", "Full interior renovation and space planning for 450 sqm waterfront villa", 4, 2, "In Design", 120000.00, "USD", "/static/images/projects/coastal_villa.jpg", "2026-11-15"),
        ("Scandinavian Penthouse", "Minimalist open-plan living room, master bedroom suite and dining layout", 5, 2, "Pending Approval", 75000.00, "USD", "/static/images/projects/nordic_penthouse.jpg", "2026-10-01"),
        ("Executive Tech HQ Office", "Ergonomic workspace design, boardroom layout and executive lounge", 6, 3, "In Progress", 180000.00, "USD", "/static/images/projects/tech_office.jpg", "2026-12-20"),
        ("Minimalist Urban Loft", "Industrial steel and warm oak concept for downtown loft apartment", 4, 3, "Approved", 55000.00, "USD", "/static/images/projects/urban_loft.jpg", "2026-09-30")
    ]

    for p in projects_data:
        db.execute(
            """INSERT INTO projects 
               (title, description, client_id, designer_id, status, budget_limit, currency, cover_image, target_completion_date) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            p
        )

    # 7. Floorplans & Canvas Data JSON
    # Realistic 2D Canvas JSON payload for room layout
    sample_canvas_json_1 = {
        "room": {
            "name": "Main Living Room & Lounge",
            "width_m": 8.0,
            "height_m": 6.0,
            "flooring_material": "Herringbone Oak Hardwood",
            "wall_color": "#F5F5F0"
        },
        "walls": [
            {"id": "w1", "x1": 50, "y1": 50, "x2": 750, "y2": 50, "thickness": 15, "color": "#2C3E50"},
            {"id": "w2", "x1": 750, "y1": 50, "x2": 750, "y2": 550, "thickness": 15, "color": "#2C3E50"},
            {"id": "w3", "x1": 750, "y1": 550, "x2": 50, "y2": 550, "thickness": 15, "color": "#2C3E50"},
            {"id": "w4", "x1": 50, "y1": 550, "x2": 50, "y2": 50, "thickness": 15, "color": "#2C3E50"}
        ],
        "openings": [
            {"id": "op1", "type": "double_door", "wall_id": "w1", "offset_m": 3.0, "width_m": 1.6, "swing_direction": "inward"},
            {"id": "op2", "type": "window", "wall_id": "w2", "offset_m": 2.0, "width_m": 2.2, "sill_height_m": 0.9}
        ],
        "objects": [
            {
                "id": "obj_sofa_1",
                "catalog_id": 1,
                "name": "Modern Velvet 3-Seater Sofa",
                "x": 220, "y": 280,
                "width": 220, "depth": 95,
                "rotation": 0,
                "z_index": 2,
                "color": "#1B4F72",
                "material": "Velvet"
            },
            {
                "id": "obj_tbl_1",
                "catalog_id": 3,
                "name": "Minimalist Scandinavian Coffee Table",
                "x": 270, "y": 390,
                "width": 120, "depth": 60,
                "rotation": 0,
                "z_index": 1,
                "color": "#F5CBA7",
                "material": "Oak"
            },
            {
                "id": "obj_rug_1",
                "catalog_id": 15,
                "name": "Large Wool Geometric Area Rug",
                "x": 180, "y": 240,
                "width": 300, "depth": 200,
                "rotation": 0,
                "z_index": 0,
                "color": "#E5E8E8",
                "material": "Wool"
            },
            {
                "id": "obj_lamp_1",
                "catalog_id": 13,
                "name": "Brass Arch Arc Floor Lamp",
                "x": 120, "y": 260,
                "width": 40, "depth": 120,
                "rotation": 45,
                "z_index": 3,
                "color": "#F1C40F"
            },
            {
                "id": "obj_plant_1",
                "catalog_id": 16,
                "name": "Fiddle Leaf Fig Indoor Plant",
                "x": 700, "y": 100,
                "width": 50, "depth": 50,
                "rotation": 0,
                "z_index": 3,
                "color": "#1E8449"
            }
        ],
        "lighting": [
            {"id": "light1", "type": "ambient", "color": "#FFF8E7", "intensity": 0.4},
            {"id": "light2", "type": "point", "x": 140, "y": 280, "radius": 220, "color": "#FEE180", "intensity": 0.85}
        ]
    }

    sample_canvas_json_2 = {
        "room": {
            "name": "Master Suite Bedroom",
            "width_m": 6.0,
            "height_m": 5.0,
            "flooring_material": "Chevron Smoked Walnut",
            "wall_color": "#8A9A86"
        },
        "walls": [
            {"id": "w1", "x1": 50, "y1": 50, "x2": 650, "y2": 50, "thickness": 15, "color": "#2C3E50"},
            {"id": "w2", "x1": 650, "y1": 50, "x2": 650, "y2": 450, "thickness": 15, "color": "#2C3E50"},
            {"id": "w3", "x1": 650, "y1": 450, "x2": 50, "y2": 450, "thickness": 15, "color": "#2C3E50"},
            {"id": "w4", "x1": 50, "y1": 450, "x2": 50, "y2": 50, "thickness": 15, "color": "#2C3E50"}
        ],
        "openings": [
            {"id": "op1", "type": "single_door", "wall_id": "w4", "offset_m": 1.0, "width_m": 0.9, "swing_direction": "inward"}
        ],
        "objects": [
            {
                "id": "obj_bed_1",
                "catalog_id": 5,
                "name": "King Size Upholstered Platform Bed",
                "x": 220, "y": 80,
                "width": 210, "depth": 200,
                "rotation": 0,
                "z_index": 2,
                "color": "#D5D8DC"
            },
            {
                "id": "obj_nst_1",
                "catalog_id": 6,
                "name": "Modern Nightstand Left",
                "x": 150, "y": 90,
                "width": 55, "depth": 45,
                "rotation": 0,
                "z_index": 1,
                "color": "#1C2833"
            },
            {
                "id": "obj_nst_2",
                "catalog_id": 6,
                "name": "Modern Nightstand Right",
                "x": 440, "y": 90,
                "width": 55, "depth": 45,
                "rotation": 0,
                "z_index": 1,
                "color": "#1C2833"
            }
        ],
        "lighting": [
            {"id": "light1", "type": "ambient", "color": "#FFF5E6", "intensity": 0.5}
        ]
    }

    floorplans_data = [
        (1, "Main Living Room Layout", "Living Room", 8.0, 6.0, 20, 50.0, json.dumps(sample_canvas_json_1), "/static/images/floorplans/living_room_thumb.png", 2),
        (1, "Master Suite Bedroom", "Bedroom", 6.0, 5.0, 20, 50.0, json.dumps(sample_canvas_json_2), "/static/images/floorplans/bedroom_thumb.png", 1),
        (2, "Scandinavian Open Concept Lounge", "Living Room", 9.0, 7.0, 20, 50.0, json.dumps(sample_canvas_json_1), "/static/images/floorplans/nordic_lounge_thumb.png", 3),
        (3, "Executive Boardroom Suite", "Office", 12.0, 8.0, 25, 40.0, json.dumps(sample_canvas_json_1), "/static/images/floorplans/office_thumb.png", 1)
    ]

    for fp in floorplans_data:
        db.execute(
            """INSERT INTO floorplans 
               (project_id, name, room_type, width_m, height_m, grid_size_cm, scale_factor, canvas_data_json, thumbnail_url, version_number) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            fp
        )

    # 8. Floorplan Versions
    db.execute(
        """INSERT INTO floorplan_versions 
           (floorplan_id, version_number, title, notes, canvas_data_json, created_by) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (1, 1, "Initial Concept Draft", "Original furniture placement before client review", json.dumps(sample_canvas_json_1), 2)
    )
    db.execute(
        """INSERT INTO floorplan_versions 
           (floorplan_id, version_number, title, notes, canvas_data_json, created_by) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (1, 2, "Revised Seating & Lighting Layout", "Added arc lamp and changed sofa fabric to Navy Velvet", json.dumps(sample_canvas_json_1), 2)
    )

    # 9. Budgets & Line Items
    db.execute(
        """INSERT INTO budgets 
           (project_id, total_estimated, total_spent, tax_rate, labor_cost, designer_margin, notes, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (1, 48500.00, 32400.00, 0.085, 4500.00, 0.15, "Primary budget allocation for living room & master suite", "Submitted")
    )
    db.execute(
        """INSERT INTO budgets 
           (project_id, total_estimated, total_spent, tax_rate, labor_cost, designer_margin, notes, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (2, 35000.00, 18200.00, 0.085, 3200.00, 0.15, "Scandinavian penthouse interior furniture & fixture package", "Draft")
    )

    budget_items = [
        (1, "Modern Velvet 3-Seater Sofa", "Living Room", "Furniture", 1850.00, 1, 1850.00, 2, "Purchased"),
        (1, "Minimalist Scandinavian Coffee Table", "Living Room", "Furniture", 480.00, 1, 480.00, 1, "Purchased"),
        (1, "King Size Upholstered Platform Bed", "Bedroom", "Furniture", 2200.00, 1, 2200.00, 3, "Ordered"),
        (1, "Herringbone Oak Hardwood Flooring (48 sqm)", "Flooring", "Material", 115.00, 48, 5520.00, 5, "Ordered"),
        (1, "Flooring & Wall Painting Installation Labor", "Labor", "Labor", 4500.00, 1, 4500.00, None, "Estimated"),
        (2, "Solid Oak 8-Seater Dining Table", "Dining", "Furniture", 2600.00, 1, 2600.00, 3, "Estimated"),
        (2, "Ergonomic Molded Dining Chairs", "Dining", "Furniture", 240.00, 8, 1920.00, 1, "Estimated")
    ]

    for bi in budget_items:
        db.execute(
            """INSERT INTO budget_line_items 
               (budget_id, item_name, category, item_type, unit_price, quantity, total_price, supplier_id, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            bi
        )

    # 10. Tasks
    tasks_data = [
        (1, "Finalize Living Room Lighting Plan", "Verify LED pendant height and switch locations with electrician", 2, "High", "In Progress", "2026-09-10", 8.0, 4.5),
        (1, "Approve Fabric Swatches with Client", "Present navy velvet and cream boucle samples to John Doe", 2, "Medium", "Completed", "2026-09-02", 4.0, 3.5),
        (1, "Confirm Flooring Material Delivery Date", "Coordinate with EcoTile & Surface Tech for warehouse dispatch", 2, "Urgent", "To Do", "2026-09-08", 2.0, 0.0),
        (2, "Review Scandinavian Penthouse Budget", "Analyze itemized costs and margin calculations for Emma Watson", 2, "High", "Under Review", "2026-09-12", 6.0, 5.0)
    ]

    for t in tasks_data:
        db.execute(
            """INSERT INTO tasks 
               (project_id, title, description, assigned_to, priority, status, due_date, estimated_hours, actual_hours) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            t
        )

    # 11. Moodboards
    moodboard_layout = {
        "grid": [
            {"type": "image", "src": "/static/images/moodboards/coastal_inspiration.jpg", "span": 2},
            {"type": "color", "hex": "#1B4F72", "label": "Deep Navy Velvet"},
            {"type": "color", "hex": "#F5CBA7", "label": "Natural Oak"},
            {"type": "color", "hex": "#F5F5F0", "label": "Alabaster White"},
            {"type": "image", "src": "/static/images/moodboards/wood_texture.jpg", "span": 1}
        ]
    }

    db.execute(
        """INSERT INTO moodboards 
           (project_id, title, description, layout_json, color_palette_json, tags, created_by) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (1, "Coastal Elegance Material Palette", "Curated materials featuring navy velvet, oak hardwood, alabaster paint and brass accents", json.dumps(moodboard_layout), '["#1B4F72", "#F5CBA7", "#F5F5F0", "#D09B69"]', "Coastal, Modern, Luxury", 2)
    )

    # 12. Comments & Annotations
    comments_data = [
        (1, 1, 4, 320.0, 310.0, "Can we consider a slightly larger coffee table to match the 3-seater sofa scale?", "Open", None),
        (1, 1, 2, 320.0, 310.0, "Great point John! We can upgrade to the 140cm Walnut variant in our next draft.", "Open", 1),
        (1, 1, 4, 700.0, 100.0, "Love the fiddle leaf fig plant placement near the main window light!", "Resolved", None)
    ]

    for c in comments_data:
        db.execute(
            """INSERT INTO comments 
               (project_id, floorplan_id, user_id, pos_x, pos_y, comment_text, status, parent_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            c
        )

    # 13. Approvals
    db.execute(
        """INSERT INTO approval_requests 
           (project_id, floorplan_id, requested_by, approved_by, status, client_notes, reviewer_notes) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (1, 1, 2, 4, "Pending", "Please review the updated living room seating layout and revised arc lamp positioning.", "Under review by John Doe")
    )

    # 14. Portfolios
    portfolios_data = [
        (2, 1, "Modern Waterfront Villa Living Space", "A serene open-plan waterfront residence combining navy velvet textures, natural oak, and floor-to-ceiling glass integration.", "/static/images/portfolio/coastal_villa_cover.jpg", "Living Room, Waterfront, Modern", 342, 48, 1),
        (2, 2, "Scandinavian Penthouse Sanctuary", "Clean lines, functional oak cabinetry, and warm sage accents define this Stockholm penthouse renovation.", "/static/images/portfolio/scandi_penthouse_cover.jpg", "Minimalist, Scandinavian, Penthouse", 518, 92, 1)
    ]

    for pf in portfolios_data:
        db.execute(
            """INSERT INTO portfolios 
               (designer_id, project_id, title, description, cover_image, tags, view_count, like_count, is_public) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            pf
        )

    # 15. Notifications
    notifications_data = [
        (4, "New Floorplan Ready for Review", "Sarah Jenkins submitted 'Main Living Room Layout' for your approval.", "Approval", 0, "/projects/1/floorplans/1"),
        (2, "Client Comment Added", "John Doe commented on floorplan 'Main Living Room Layout'.", "Info", 0, "/projects/1/floorplans/1"),
        (2, "Inventory Alert", "Herringbone Oak Hardwood stock is low at Nordic Design Co.", "Warning", 0, "/inventory")
    ]

    for n in notifications_data:
        db.execute(
            """INSERT INTO notifications 
               (user_id, title, message, type, is_read, target_url) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            n
        )

    # 16. Audit Logs
    audit_data = [
        (2, "USER_LOGIN", "User", 2, '{"email": "sarah.jenkins@dreamhome.com"}', "127.0.0.1", "Mozilla/5.0"),
        (2, "FLOORPLAN_UPDATE", "Floorplan", 1, '{"version": 2, "action": "saved_layout"}', "127.0.0.1", "Mozilla/5.0"),
        (4, "COMMENT_CREATED", "Comment", 1, '{"floorplan_id": 1, "text_snippet": "Can we consider a slightly..."}', "127.0.0.1", "Mozilla/5.0")
    ]

    for a in audit_data:
        db.execute(
            """INSERT INTO audit_logs 
               (user_id, action, entity_type, entity_id, details_json, ip_address, user_agent) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            a
        )

    print("Database successfully seeded with realistic sample data!")

if __name__ == "__main__":
    seed_database()
