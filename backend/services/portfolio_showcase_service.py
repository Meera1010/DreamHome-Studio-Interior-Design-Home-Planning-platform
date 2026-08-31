"""
DreamHome Studio — Portfolio Showcase & Public Engagement Service
Manages public portfolio galleries, view/like increments, shareable token generation,
and designer showcase statistics.
"""

import hashlib
from typing import Dict, Any, List, Optional
from database.db_manager import get_db
from backend.models.portfolio import Portfolio

class PortfolioShowcaseService:
    """Public designer portfolio gallery & engagement engine."""

    @staticmethod
    def increment_views(portfolio_id: int) -> int:
        """Increment public view counter for a portfolio showcase item."""
        db = get_db()
        db.execute("UPDATE portfolios SET view_count = view_count + 1 WHERE id = ?;", (portfolio_id,))
        res = db.query_one("SELECT view_count FROM portfolios WHERE id = ?;", (portfolio_id,))
        return res["view_count"] if res else 0

    @staticmethod
    def increment_likes(portfolio_id: int) -> int:
        """Increment like counter for a portfolio showcase item."""
        db = get_db()
        db.execute("UPDATE portfolios SET like_count = like_count + 1 WHERE id = ?;", (portfolio_id,))
        res = db.query_one("SELECT like_count FROM portfolios WHERE id = ?;", (portfolio_id,))
        return res["like_count"] if res else 0

    @staticmethod
    def generate_shareable_link(portfolio_id: int) -> str:
        """Generate a cryptographically signed shareable link token for client previews."""
        salt = "dh_portfolio_share_salt_7719"
        raw = f"{portfolio_id}:{salt}"
        token = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        return f"/portfolio/share/{portfolio_id}?token={token}"

    @staticmethod
    def get_designer_portfolio_stats(designer_id: int) -> Dict[str, Any]:
        """Aggregate total views, likes, and showcases count for a designer."""
        db = get_db()
        res = db.query_one(
            """SELECT COUNT(*) as total_showcases, 
                      SUM(view_count) as total_views, 
                      SUM(like_count) as total_likes 
               FROM portfolios WHERE designer_id = ?;""",
            (designer_id,)
        )
        return {
            "total_showcases": res["total_showcases"] if res else 0,
            "total_views": res["total_views"] or 0 if res else 0,
            "total_likes": res["total_likes"] or 0 if res else 0
        }
