"""
DreamHome Studio — Extended Catalog Query & Taxonomy Service
Provides rich multi-attribute search, category filtering, price range grouping,
dimensional spatial bounding box filters, and brand aggregations for interior furnishings.
"""

from typing import List, Dict, Any, Optional
from database.db_manager import get_db
from backend.models.furniture import FurnitureCatalog
from backend.models.material import MaterialCatalog

class ExtendedCatalogService:
    """Advanced search and indexing service for catalog items and surface materials."""

    @staticmethod
    def search_furniture_advanced(
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        query: Optional[str] = None,
        brand: Optional[str] = None,
        material: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        max_width_cm: Optional[float] = None,
        max_depth_cm: Optional[float] = None,
        sort_by: str = "name_asc",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Perform multi-criteria filtered search across furniture catalog records.
        """
        sql = "SELECT * FROM furniture_catalog WHERE 1=1"
        params = []

        if category and category.lower() != "all":
            sql += " AND LOWER(category) = LOWER(?)"
            params.append(category)

        if subcategory and subcategory.lower() != "all":
            sql += " AND LOWER(subcategory) = LOWER(?)"
            params.append(subcategory)

        if query:
            sql += " AND (LOWER(name) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(sku) LIKE ? OR LOWER(material) LIKE ?)"
            term = f"%{query.lower().strip()}%"
            params.extend([term, term, term, term])

        if brand and brand.lower() != "all":
            sql += " AND LOWER(brand) = LOWER(?)"
            params.append(brand)

        if material and material.lower() != "all":
            sql += " AND LOWER(material) = LOWER(?)"
            params.append(material)

        if min_price is not None:
            sql += " AND price >= ?"
            params.append(min_price)

        if max_price is not None:
            sql += " AND price <= ?"
            params.append(max_price)

        if max_width_cm is not None:
            sql += " AND width_cm <= ?"
            params.append(max_width_cm)

        if max_depth_cm is not None:
            sql += " AND depth_cm <= ?"
            params.append(max_depth_cm)

        # Sorting
        sort_map = {
            "name_asc": "name ASC",
            "name_desc": "name DESC",
            "price_asc": "price ASC",
            "price_desc": "price DESC",
            "newest": "id DESC"
        }
        order_clause = sort_map.get(sort_by, "name ASC")
        sql += f" ORDER BY {order_clause}"

        db = get_db()

        # Count total matching rows
        count_sql = f"SELECT COUNT(*) as cnt FROM ({sql});"
        count_res = db.query_one(count_sql, tuple(params))
        total_items = count_res["cnt"] if count_res else 0

        # Pagination
        offset = (max(1, page) - 1) * page_size
        sql += " LIMIT ? OFFSET ?;"
        params.extend([page_size, offset])

        rows = db.query_all(sql, tuple(params))
        items = [FurnitureCatalog.from_row(r).to_dict() for r in rows]

        return {
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_items + page_size - 1) // page_size if page_size > 0 else 1,
            "items": items
        }

    @staticmethod
    def get_catalog_facets() -> Dict[str, Any]:
        """
        Return category, brand, and material facet counts for frontend filter sidebars.
        """
        db = get_db()
        
        categories = db.query_all(
            "SELECT category, COUNT(*) as count FROM furniture_catalog GROUP BY category ORDER BY count DESC;"
        )
        brands = db.query_all(
            "SELECT brand, COUNT(*) as count FROM furniture_catalog WHERE brand IS NOT NULL GROUP BY brand ORDER BY count DESC;"
        )
        materials = db.query_all(
            "SELECT material, COUNT(*) as count FROM furniture_catalog WHERE material IS NOT NULL GROUP BY material ORDER BY count DESC;"
        )
        price_stats = db.query_one(
            "SELECT MIN(price) as min_price, MAX(price) as max_price, AVG(price) as avg_price FROM furniture_catalog;"
        )

        return {
            "categories": [{"category": r["category"], "count": r["count"]} for r in categories],
            "brands": [{"brand": r["brand"], "count": r["count"]} for r in brands],
            "materials": [{"material": r["material"], "count": r["count"]} for r in materials],
            "price_stats": {
                "min_price": float(price_stats["min_price"] or 0.0),
                "max_price": float(price_stats["max_price"] or 0.0),
                "avg_price": round(float(price_stats["avg_price"] or 0.0), 2)
            }
        }
