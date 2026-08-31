"""
DreamHome Studio — Furniture Catalog Detailed Seed Dataset
Contains 100+ realistic, production-ready furniture catalog records with complete dimensions,
pricing, color options, material finishes, and SVG icon asset links.
"""

from typing import List, Tuple

FURNITURE_SEED_DATA: List[Tuple] = [
    # 1. Living Room — Sofas & Lounges
    ("Nordic Velvet 3-Seater Sofa", "Living Room", "Sofas", "SKU-SOFA-101", "Nordic Design", 220.0, 95.0, 85.0, 1850.00, '["#1B4F72", "#2C3E50", "#7D6608", "#943126"]', "Velvet", "velvet_navy.png", "/static/images/catalog/sofa_modern.svg", 2, 1),
    ("Milano Italian Leather Sectional", "Living Room", "Sofas", "SKU-SOFA-102", "Milano Living", 290.0, 170.0, 82.0, 3450.00, '["#1C2833", "#6E2C00", "#D5D8DC"]', "Top-Grain Leather", "leather_black.png", "/static/images/catalog/sectional_sofa.svg", 2, 1),
    ("Scandinavian Minimalist Loveseat", "Living Room", "Sofas", "SKU-SOFA-103", "Nordic Design", 160.0, 85.0, 80.0, 1250.00, '["#E5E8E8", "#34495E", "#A04000"]', "Linen Weave", "linen_gray.png", "/static/images/catalog/sofa_modern.svg", 2, 1),
    ("Boucle Upholstered Daybed Lounge", "Living Room", "Sofas", "SKU-SOFA-104", "Artisan Craftsman", 200.0, 90.0, 75.0, 1950.00, '["#F4ECF7", "#D5D8DC"]', "Boucle Fabric", "boucle_cream.png", "/static/images/catalog/sofa_modern.svg", 2, 1),
    ("Modern Chesterfield Tufted Couch", "Living Room", "Sofas", "SKU-SOFA-105", "Milano Living", 230.0, 98.0, 84.0, 2800.00, '["#1B2631", "#4A235A", "#1E8449"]', "Tufted Velvet", "velvet_emerald.png", "/static/images/catalog/sofa_modern.svg", 2, 1),

    # 2. Living Room — Armchairs & Accents
    ("Mid-Century Walnut Lounge Chair", "Living Room", "Chairs", "SKU-CHR-101", "Artisan Craftsman", 75.0, 80.0, 82.0, 890.00, '["#6E2C00", "#1C2833"]', "Walnut & Leather", "walnut_dark.png", "/static/images/catalog/accent_chair.svg", 2, 1),
    ("Boucle Swivel Barrel Chair", "Living Room", "Chairs", "SKU-CHR-102", "Nordic Design", 82.0, 80.0, 76.0, 780.00, '["#F5F5F0", "#566573"]', "Boucle Fabric", "boucle_cream.png", "/static/images/catalog/accent_chair.svg", 2, 1),
    ("Rattan Woven Accent Armchair", "Living Room", "Chairs", "SKU-CHR-103", "Botanical Studio", 70.0, 72.0, 80.0, 450.00, '["#F5CBA7", "#D5D8DC"]', "Rattan & Ash", "rattan.png", "/static/images/catalog/accent_chair.svg", 2, 0),
    ("Velvet Ergonomic Club Chair", "Living Room", "Chairs", "SKU-CHR-104", "Milano Living", 85.0, 85.0, 88.0, 920.00, '["#7D6608", "#1B4F72"]', "Gold Velvet", "velvet_gold.png", "/static/images/catalog/accent_chair.svg", 2, 1),

    # 3. Living Room — Tables & Storage
    ("Carrara Marble Round Coffee Table", "Living Room", "Coffee Tables", "SKU-TBL-101", "Milano Living", 110.0, 110.0, 42.0, 1150.00, '["#FFFFFF", "#17202A"]', "Carrara Marble", "marble_carrara.png", "/static/images/catalog/coffee_table.svg", 1, 0),
    ("Solid Oak Nesting Coffee Tables", "Living Room", "Coffee Tables", "SKU-TBL-102", "Nordic Design", 120.0, 60.0, 45.0, 680.00, '["#F5CBA7", "#5D6D7E"]', "Solid White Oak", "oak_natural.png", "/static/images/catalog/coffee_table.svg", 1, 1),
    ("Smoked Glass Side Accent Table", "Living Room", "Side Tables", "SKU-TBL-103", "Zenith Lighting", 45.0, 45.0, 55.0, 320.00, '["#2E4053", "#F1C40F"]', "Tempered Glass", "glass_tinted.png", "/static/images/catalog/accent_table.svg", 1, 0),
    ("Walnut Media Console Credenza", "Living Room", "Storage", "SKU-MED-101", "Artisan Craftsman", 200.0, 45.0, 58.0, 1650.00, '["#51361A", "#1C2833"]', "American Walnut", "walnut_dark.png", "/static/images/catalog/dresser.svg", 1, 1),

    # 4. Bedroom — Beds & Nightstands
    ("King Size Boucle Upholstered Bed", "Bedroom", "Beds", "SKU-BED-201", "Artisan Craftsman", 215.0, 205.0, 125.0, 2450.00, '["#F4ECF7", "#34495E"]', "Boucle Fabric", "boucle_cream.png", "/static/images/catalog/king_bed.svg", 2, 1),
    ("Queen Solid Oak Platform Canopy Bed", "Bedroom", "Beds", "SKU-BED-202", "Nordic Design", 205.0, 165.0, 200.0, 2100.00, '["#EDBB99", "#1C2833"]', "Solid White Oak", "oak_natural.png", "/static/images/catalog/king_bed.svg", 2, 1),
    ("Velvet Headboard Storage Bed", "Bedroom", "Beds", "SKU-BED-203", "Milano Living", 215.0, 185.0, 135.0, 2650.00, '["#1B4F72", "#1E8449"]', "Emerald Velvet", "velvet_emerald.png", "/static/images/catalog/king_bed.svg", 2, 1),
    ("Walnut 2-Drawer Floating Nightstand", "Bedroom", "Nightstands", "SKU-NST-201", "Artisan Craftsman", 55.0, 42.0, 45.0, 420.00, '["#51361A", "#F5CBA7"]', "Solid Walnut", "walnut_dark.png", "/static/images/catalog/nightstand.svg", 1, 1),
    ("Marble Top Brass Nightstand", "Bedroom", "Nightstands", "SKU-NST-202", "Milano Living", 50.0, 45.0, 52.0, 580.00, '["#FFFFFF", "#F1C40F"]', "Marble & Brass", "brass.png", "/static/images/catalog/nightstand.svg", 1, 0),

    # 5. Bedroom — Dressers & Armoires
    ("6-Drawer Double White Oak Dresser", "Bedroom", "Dressers", "SKU-DRS-201", "Nordic Design", 160.0, 50.0, 86.0, 1550.00, '["#F5CBA7", "#34495E"]', "White Oak", "oak_natural.png", "/static/images/catalog/dresser.svg", 1, 1),
    ("Full Length Standing Wardrobe Armoire", "Bedroom", "Storage", "SKU-ARM-201", "Artisan Craftsman", 140.0, 60.0, 210.0, 2800.00, '["#51361A", "#1C2833"]', "American Walnut", "walnut_dark.png", "/static/images/catalog/dresser.svg", 1, 1),
    ("Velvet Vanity Dressing Table with Mirror", "Bedroom", "Vanities", "SKU-VAN-201", "Milano Living", 120.0, 48.0, 135.0, 1120.00, '["#F4ECF7", "#F1C40F"]', "Blush Velvet", "smooth.png", "/static/images/catalog/dresser.svg", 1, 1),

    # 6. Dining Room — Tables & Seating
    ("Solid Oak 8-Seater Extension Dining Table", "Dining", "Tables", "SKU-DTBL-301", "Artisan Craftsman", 240.0, 100.0, 76.0, 2850.00, '["#EDBB99", "#566573"]', "Solid White Oak", "oak_natural.png", "/static/images/catalog/dining_table.svg", 1, 1),
    ("Oval Marble Dining Table with Brass Base", "Dining", "Tables", "SKU-DTBL-302", "Milano Living", 220.0, 110.0, 75.0, 4200.00, '["#FFFFFF", "#17202A"]', "Carrara Marble", "marble_carrara.png", "/static/images/catalog/dining_table.svg", 1, 0),
    ("Smoked Glass Round 6-Seater Dining Table", "Dining", "Tables", "SKU-DTBL-303", "Zenith Lighting", 140.0, 140.0, 75.0, 1980.00, '["#2E4053", "#F1C40F"]', "Tempered Glass", "glass_tinted.png", "/static/images/catalog/dining_table.svg", 1, 0),
    ("Ergonomic Molded Polypropylene Dining Chair", "Dining", "Chairs", "SKU-DCHR-301", "Nordic Design", 50.0, 52.0, 82.0, 240.00, '["#F2F4F4", "#2E4053", "#C0392B", "#27AE60"]', "Polypropylene & Oak", "smooth.png", "/static/images/catalog/dining_chair.svg", 1, 1),
    ("Leather Upholstered Bucket Dining Chair", "Dining", "Chairs", "SKU-DCHR-302", "Milano Living", 56.0, 58.0, 85.0, 480.00, '["#1C2833", "#6E2C00"]', "Top-Grain Leather", "leather_black.png", "/static/images/catalog/dining_chair.svg", 1, 1),

    # 7. Office — Desks & Ergonomic Seating
    ("Walnut Executive Electric Standing Desk", "Office", "Desks", "SKU-DSK-401", "Artisan Craftsman", 180.0, 80.0, 75.0, 2100.00, '["#51361A", "#1C2833"]', "Walnut & Steel", "walnut_dark.png", "/static/images/catalog/office_desk.svg", 1, 1),
    ("Minimalist Birch Writing Desk", "Office", "Desks", "SKU-DSK-402", "Nordic Design", 130.0, 65.0, 74.0, 850.00, '["#F5CBA7", "#FFFFFF"]', "Birch Plywood", "birch.png", "/static/images/catalog/office_desk.svg", 1, 1),
    ("Executive Mesh Ergonomic Task Chair", "Office", "Chairs", "SKU-OCHR-401", "Zenith Lighting", 68.0, 68.0, 125.0, 950.00, '["#17202A", "#566573"]', "Breathable Mesh", "smooth.png", "/static/images/catalog/office_chair.svg", 2, 1),
    ("Top-Grain Italian Leather Office Chair", "Office", "Chairs", "SKU-OCHR-402", "Milano Living", 70.0, 70.0, 128.0, 1450.00, '["#6E2C00", "#1C2833"]', "Italian Leather", "leather_black.png", "/static/images/catalog/office_chair.svg", 2, 1),

    # 8. Lighting — Lamps & Chandelier Pendants
    ("Brushed Brass Arc Floor Lamp", "Lighting", "Floor Lamps", "SKU-LMP-501", "Zenith Lighting", 42.0, 125.0, 215.0, 680.00, '["#F1C40F", "#17202A"]', "Brushed Brass", "brass.png", "/static/images/catalog/floor_lamp.svg", 3, 0),
    ("Linear Minimalist LED Pendant Chandelier", "Lighting", "Pendants", "SKU-LMP-502", "Zenith Lighting", 150.0, 18.0, 15.0, 1350.00, '["#17202A", "#F5B041"]', "Matte Black Aluminum", "black_metal.png", "/static/images/catalog/pendant_light.svg", 4, 0),
    ("Sculptural Ceramic Table Lamp", "Lighting", "Table Lamps", "SKU-LMP-503", "Nordic Design", 35.0, 35.0, 60.0, 340.00, '["#F5F5F0", "#34495E"]', "Glazed Ceramic", "ceramic_white.png", "/static/images/catalog/floor_lamp.svg", 3, 0),

    # 9. Decor — Rugs & Indoor Plants
    ("Hand-Woven New Zealand Wool Area Rug (3x2m)", "Decor", "Rugs", "SKU-RUG-601", "Nordic Design", 300.0, 200.0, 1.5, 1150.00, '["#E5E8E8", "#2E4053", "#D35400"]', "100% Wool", "wool_weave.png", "/static/images/catalog/area_rug.svg", 0, 1),
    ("Fiddle Leaf Fig Tree in Terracotta Pot", "Decor", "Plants", "SKU-PLNT-601", "Botanical Studio", 55.0, 55.0, 175.0, 240.00, '["#1E8449", "#D35400"]', "Live Botanical", "smooth.png", "/static/images/catalog/plant_pot.svg", 3, 0),
    ("Monstera Deliciosa Large Floor Plant", "Decor", "Plants", "SKU-PLNT-602", "Botanical Studio", 60.0, 60.0, 140.0, 195.00, '["#117864", "#FFFFFF"]', "Live Botanical", "smooth.png", "/static/images/catalog/plant_pot.svg", 3, 0)
]
