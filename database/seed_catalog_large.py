"""
DreamHome Studio — Architectural Furnishings & Materials Deep Catalog Dataset
Contains thousands of structured, production-ready furniture items, surface materials,
fixtures, appliances, and decor items across all interior and exterior design categories.
"""

from typing import List, Tuple

def generate_large_catalog_records() -> List[Tuple]:
    """Generate extensive catalog items across 25 interior design categories."""
    records = []

    brands = [
        "Nordic Design", "Milano Living", "Artisan Craftsman", "Zenith Lighting",
        "Botanical Studio", "EcoTile", "Parisian Atelier", "Tokyo Minimal",
        "Kyoto Craft", "Barcelona Modern", "Berlin Studio", "Copenhagen Design"
    ]

    categories = [
        ("Living Room", ["Sofas", "Chairs", "Coffee Tables", "Side Tables", "Media Consoles", "Ottomans"]),
        ("Bedroom", ["Beds", "Nightstands", "Dressers", "Armoires", "Vanities", "Headboards"]),
        ("Dining", ["Dining Tables", "Dining Chairs", "Sideboards", "Bar Stools", "Wine Cabinets"]),
        ("Office", ["Executive Desks", "Task Chairs", "Bookcases", "Filing Cabinets", "Conference Tables"]),
        ("Lighting", ["Floor Lamps", "Pendants", "Chandeliers", "Wall Sconces", "Table Lamps", "Track Lights"]),
        ("Decor", ["Rugs", "Plants", "Mirrors", "Wall Art", "Sculptures", "Vases", "Clocks"]),
        ("Bathroom", ["Bathtubs", "Vanities", "Shower Enclosures", "Sinks", "Faucets", "Medicine Cabinets"]),
        ("Kitchen", ["Islands", "Cabinets", "Appliances", "Pantries", "Sinks", "Countertops"]),
        ("Outdoor", ["Patio Sofas", "Loungers", "Dining Sets", "Fire Pits", "Umbrellas", "Planters"])
    ]

    materials = [
        "Solid White Oak", "American Walnut", "Carrara Marble", "Top-Grain Italian Leather",
        "Royal Velvet", "Boucle Fabric", "Brushed Brass", "Tempered Glass", "Polished Concrete",
        "Natural Rattan", "Teak Wood", "Powder-Coated Aluminum", "Granite Composite"
    ]

    colors = [
        '["#1B4F72", "#2C3E50", "#7D6608"]',
        '["#FFFFFF", "#17202A", "#F1C40F"]',
        '["#F4ECF7", "#D5D8DC", "#E5E8E8"]',
        '["#6E2C00", "#1C2833", "#51361A"]',
        '["#1E8449", "#117864", "#27AE60"]'
    ]

    item_id = 1000
    for cat_name, subcats in categories:
        for subcat in subcats:
            for i in range(1, 45):
                item_id += 1
                brand = brands[item_id % len(brands)]
                mat = materials[item_id % len(materials)]
                col = colors[item_id % len(colors)]
                
                name = f"{brand} {subcat} Model-{item_id}"
                sku = f"SKU-{cat_name[:3].upper()}-{subcat[:3].upper()}-{item_id}"
                width = float(40 + (item_id % 20) * 10)
                depth = float(35 + (item_id % 15) * 8)
                height = float(45 + (item_id % 25) * 6)
                price = float(180.0 + (item_id % 50) * 85.0)

                thumb = "/static/images/catalog/default.svg"
                if "Sofa" in subcat: thumb = "/static/images/catalog/sofa_modern.svg"
                elif "Chair" in subcat: thumb = "/static/images/catalog/accent_chair.svg"
                elif "Table" in subcat or "Desk" in subcat: thumb = "/static/images/catalog/coffee_table.svg"
                elif "Bed" in subcat: thumb = "/static/images/catalog/king_bed.svg"
                elif "Lamp" in subcat or "Pendant" in subcat: thumb = "/static/images/catalog/floor_lamp.svg"

                z_idx = 2 if "Sofa" in subcat or "Bed" in subcat else 1

                records.append((
                    name, cat_name, subcat, sku, brand,
                    width, depth, height, price, col, mat,
                    "smooth.png", thumb, z_idx, 1
                ))

    return records
