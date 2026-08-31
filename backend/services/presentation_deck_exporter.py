"""
DreamHome Studio — Presentation Deck & PDF Exporter Service
Synthesizes client presentation decks, moodboard slide layouts,
and itemized specification sheets.
"""

from typing import List, Dict, Any

class PresentationDeckExporter:
    """Exporter service for client slide decks and design portfolios."""

    @staticmethod
    def compile_presentation_slides(project_data: Dict[str, Any], moodboard: Dict[str, Any], budget: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate structured slide deck payload for client presentations."""
        slides = []
        
        # Slide 1: Cover Slide
        slides.append({
            "slide_number": 1,
            "type": "COVER",
            "title": project_data.get("title", "Interior Design Concept"),
            "subtitle": f"Prepared for {project_data.get('client_name', 'Valued Client')}",
            "designer": project_data.get("designer_name", "Lead Interior Designer"),
            "date": "2026-08-31"
        })
        
        # Slide 2: Design Moodboard & Color Palette
        slides.append({
            "slide_number": 2,
            "type": "MOODBOARD",
            "title": "Design Concept & Color Palette",
            "color_swatches": moodboard.get("color_palette", ["#1C2833", "#F5CBA7", "#FFFFFF"]),
            "materials": moodboard.get("materials", ["European Oak", "Calacatta Marble", "Brushed Brass"])
        })
        
        # Slide 3: 2D Interactive Floor Plan
        slides.append({
            "slide_number": 3,
            "type": "FLOORPLAN",
            "title": "2D Space Planning & Layout",
            "room_area_sqm": project_data.get("area_sqm", 48.0),
            "total_items_count": len(project_data.get("furniture_items", []))
        })
        
        # Slide 4: Budget Breakdown
        slides.append({
            "slide_number": 4,
            "type": "FINANCIAL_SUMMARY",
            "title": "Investment & Budget Schedule",
            "total_estimated": budget.get("total_cost", 0.0),
            "furniture_total": budget.get("furniture_total", 0.0),
            "finishes_total": budget.get("finishes_total", 0.0),
            "labor_tax_total": budget.get("labor_tax", 0.0)
        })
        
        return slides
