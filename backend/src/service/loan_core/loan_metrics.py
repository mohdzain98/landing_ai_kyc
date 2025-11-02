class LoanMetrics:
    def __init__(self):
        pass

    def compute(self, kpi_result):
        income = kpi_result["aggregate"]["income_total"]
        avg_balance = kpi_result["aggregate"]["avg_balance_total"]

        metrics = {
            "fico_mid": 730,
            "dti_front": round(0.28, 2),
            "ltv": round(0.7, 2),
            "reserves_months": round(avg_balance / (income + 1), 2),
            "income_stability": 0.9
        }

        return metrics
