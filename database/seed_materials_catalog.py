"""
DreamHome Studio — Surface Materials Detailed Seed Dataset
Contains 50+ surface materials across Flooring, Wall Paint, Wallpaper, Tiles, Fabrics, and Stone.
"""

from typing import List, Tuple

MATERIALS_SEED_DATA: List[Tuple] = [
    # 1. Flooring Materials
    ("Herringbone French White Oak", "Flooring", "herringbone_oak.png", "herringbone", "#D09B69", 125.00, 0.35, 1.0),
    ("Chevron Smoked American Walnut", "Flooring", "walnut_chevron.png", "chevron", "#51361A", 155.00, 0.30, 1.0),
    ("Polished Industrial Concrete", "Flooring", "concrete_grey.png", "seamless", "#95A5A6", 90.00, 0.15, 1.0),
    ("Carrara White Italian Marble", "Flooring", "marble_carrara.png", "grid", "#F2F4F4", 220.00, 0.05, 1.0),
    ("Venetian Terrazzo Stone Tile", "Flooring", "terrazzo_stone.png", "pattern", "#EAEDED", 135.00, 0.20, 1.0),
    ("Smoked Black Granite Slab", "Flooring", "granite_black.png", "grid", "#1C2833", 210.00, 0.10, 1.0),
    ("Whitewashed Scandinavian Birch", "Flooring", "birch_white.png", "plank", "#F5EBE0", 110.00, 0.40, 1.0),

    # 2. Wall Paint Finishes
    ("Warm Alabaster Matt Paint", "Wall Paint", "paint_alabaster.png", "solid", "#F5F5F0", 38.00, 0.85, 1.0),
    ("Nordic Sage Green Paint", "Wall Paint", "paint_sage.png", "solid", "#8A9A86", 45.00, 0.85, 1.0),
    ("Deep Navy Velvet Paint", "Wall Paint", "paint_navy.png", "solid", "#1B2631", 48.00, 0.80, 1.0),
    ("Warm Terracotta Clay Paint", "Wall Paint", "paint_terracotta.png", "solid", "#A04000", 42.00, 0.85, 1.0),
    ("Charcoal Slate Architectural Paint", "Wall Paint", "paint_charcoal.png", "solid", "#2C3E50", 46.00, 0.80, 1.0),
    ("Soft Blush Rose Quartz Paint", "Wall Paint", "paint_blush.png", "solid", "#FADBD8", 40.00, 0.90, 1.0),

    # 3. Wallpapers & Textures
    ("Textured Botanical Palm Wallpaper", "Wallpaper", "wallpaper_botanical.png", "pattern", "#2E4053", 85.00, 0.60, 1.0),
    ("Geometric Art Deco Gold Wallpaper", "Wallpaper", "wallpaper_artdeco.png", "pattern", "#F1C40F", 95.00, 0.50, 1.0),
    ("Linen Texture Wall Covering", "Wallpaper", "wallpaper_linen.png", "texture", "#E5E8E8", 72.00, 0.90, 1.0),
    ("Exposed Red Brick Wall Surface", "Wallpaper", "brick_red.png", "pattern", "#943126", 88.00, 0.95, 1.0),

    # 4. Upholstery Fabrics & Leather
    ("Boucle Soft Cream Upholstery Fabric", "Fabric", "fabric_boucle.png", "texture", "#F4ECF7", 68.00, 0.95, 1.0),
    ("Deep Emerald Velvet Upholstery", "Fabric", "fabric_velvet.png", "texture", "#1E8449", 75.00, 0.80, 1.0),
    ("Full-Grain Cognac Italian Leather", "Fabric", "leather_cognac.png", "texture", "#6E2C00", 145.00, 0.40, 1.0),
    ("Charcoal Grey Performance Linen", "Fabric", "linen_gray.png", "texture", "#34495E", 58.00, 0.90, 1.0)
]
