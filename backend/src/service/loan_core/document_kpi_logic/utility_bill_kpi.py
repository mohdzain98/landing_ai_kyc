from datetime import datetime

class UtilityKPI:
    """
    Calculate utility-bill underwriting KPIs:
      - Utility Payment Amount
      - Utility Payment Stability Indicator
      - Billing Recency Check
    """

    @staticmethod
    def _parse_amount(val):
        """Convert '$89.14' -> 89.14 safely"""
        try:
            return float(str(val).replace("$", "").replace(",", "").strip()) if val else 0.0
        except:
            return 0.0

    def calculate(self, data: dict) -> dict:
        # Extract values
        total_due = self._parse_amount(data.get("total_amount_due"))
        prev_balance = self._parse_amount(data.get("amount_due_previous_statement"))
        unpaid_balance = self._parse_amount(data.get("current_unpaid_balance"))

        # KPI 1 — Utility Payment Amount
        utility_payment_amount = round(total_due, 2)

        # KPI 2 — Payment Stability
        if unpaid_balance == 0 and prev_balance == 0:
            payment_stability = "On-time payer"
        else:
            payment_stability = "Possible late or outstanding balance"

        # KPI 3 — Billing Recency
        bill_date = datetime.strptime(data["statement_date"], "%Y-%m-%d")
        days_old = (datetime.today() - bill_date).days
        billing_recency = "Recent bill" if days_old <= 90 else "Old bill — request latest bill"

        return {
            "Utility Payment Amount": utility_payment_amount,
            "Utility Payment Stability Indicator": payment_stability,
            "Billing Recency Check": billing_recency
        }
