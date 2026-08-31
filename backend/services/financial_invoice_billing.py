"""
DreamHome Studio — Financial Invoice & Billing Service
Provides multi-currency calculations, regional tax rates, contractor splits,
milestone billing schedules, and PDF invoice payload generation.
"""

from typing import List, Dict, Any

class FinancialInvoiceBillingService:
    """Enterprise billing and financial management service."""

    CURRENCY_RATES = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "CAD": 1.36,
        "AUD": 1.52,
        "JPY": 155.0
    }

    TAX_RATES_BY_REGION = {
        "US_CA": 0.0925,
        "US_NY": 0.08875,
        "UK": 0.20,
        "EU_DE": 0.19,
        "EU_FR": 0.20,
        "CA_ON": 0.13
    }

    @staticmethod
    def calculate_milestone_schedule(project_total: float, milestone_percents: List[float] = None) -> List[Dict[str, Any]]:
        """Generate milestone billing schedule for interior design project."""
        if not milestone_percents:
            milestone_percents = [20.0, 30.0, 30.0, 20.0]  # Deposit, Design Approval, Procurement, Final Handover
            
        milestone_names = [
            "1. Initial Deposit & Spatial Concept",
            "2. Design Approval & 2D CAD Drawings",
            "3. Furniture Procurement & Order Placement",
            "4. Final Site Installation & Handover"
        ]
        
        schedule = []
        for i, pct in enumerate(milestone_percents):
            amount = round(project_total * (pct / 100.0), 2)
            schedule.append({
                "milestone_number": i + 1,
                "name": milestone_names[i] if i < len(milestone_names) else f"Milestone Phase {i+1}",
                "percentage": pct,
                "amount": amount,
                "status": "Pending" if i > 0 else "Due Upon Signing"
            })
        return schedule

    @staticmethod
    def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
        """Convert financial figures across supported ISO currencies."""
        rate_from = FinancialInvoiceBillingService.CURRENCY_RATES.get(from_curr.upper(), 1.0)
        rate_to = FinancialInvoiceBillingService.CURRENCY_RATES.get(to_curr.upper(), 1.0)
        
        usd_amount = amount / rate_from
        converted = usd_amount * rate_to
        return round(converted, 2)

    @staticmethod
    def generate_invoice_payload(project_id: int, client_name: str, line_items: List[Dict[str, Any]], region_code: str = "US_CA") -> Dict[str, Any]:
        """Synthesize detailed tax-adjusted invoice payload."""
        subtotal = sum(item.get("price", 0.0) * item.get("quantity", 1) for item in line_items)
        tax_rate = FinancialInvoiceBillingService.TAX_RATES_BY_REGION.get(region_code, 0.08)
        tax_amount = round(subtotal * tax_rate, 2)
        total_due = round(subtotal + tax_amount, 2)
        
        return {
            "project_id": project_id,
            "client_name": client_name,
            "line_items_count": len(line_items),
            "subtotal": round(subtotal, 2),
            "region_code": region_code,
            "tax_rate_percent": round(tax_rate * 100.0, 2),
            "tax_amount": tax_amount,
            "total_due": total_due,
            "currency": "USD"
        }
