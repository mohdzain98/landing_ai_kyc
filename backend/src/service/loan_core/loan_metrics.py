from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import json
import argparse


sample_input = bank_statement_kpis = {
    "average_monthly_transaction_count": 1.23,
    "monthly_average_debit": 114.87,
    "monthly_average_credit": 56.2,
    "average_monthly_debit_credit_ratio": 2.0437,
    "average_monthly_balance": -170.74
}
credit_report_kpis = {
    "representative_credit_score": 609,
    "secondary_score": 586,
    "credit_score_band": "poor",
    "credit_history": {
        "total_accounts": 29,
        "open_tradelines": 4,
        "revolving_accounts": 2,
        "installment_accounts": 2,
        "mortgage_accounts": 0,
        "credit_mix_strength": "adequate_mix"
    },
    "credit_age": {
        "average_account_age_months": 68,
        "file_age_years": 8.75,
        "oldest_account_open_date": "2010-09",
        "recent_account_open_months_ago": 29
    },
    "delinquency_profile": {
        "30_day_delinquencies": 1,
        "60_day_delinquencies": 0,
        "90_day_delinquencies": 0,
        "has_recent_delinquency": True,
        "overall_delinquency_risk": "minor_recent_issue"
    },
    "negative_events": {
        "bankruptcies": 0,
        "collections": 0,
        "is_clean_from_major_derogatory": True
    },
    "inquiry_profile": {
        "recent_hard_inquiries_180d": None,
        "inquiry_risk": "unknown"
    },
    "exposure_profile": {
        "maximum_total_principal": None,
        "current_principal_balance": 6200.0
    }
}

identity_doc_kpis = {
    "age": 40,
    "document_valid": True,
    "days_until_expiry": 3297,
    "document_verification_status": "valid",
    "issuing_country": "UNITED STATES OF AMERICA",
    "has_passport_number": True,
    "has_address": False
}

income_proof_kpis = {
    "Gross Monthly Income": 7600.0,
    "paystub_recency_days": 827,
    "total_deductions": 2100.0,
    "recency_check": "Old paystub — request newer",
    "stability_flag": "stable"
}

tax_statement_kpis = {
    "Gross Monthly Income": 5700.0,
    "Estimated Take-Home Pay": 4446.0,
    "Income Type": "Salaried (W-2)",
    "Income Stability Indicator": "Stable Income",
    "Taxable-Income Ratio": 0.79
}

utility_bill_kpis = {
    "Utility Payment Amount": 89.14,
    "Utility Payment Stability Indicator": "On-time payer",
    "Billing Recency Check": "Old bill — request latest bill"
}

all_kpis = {
    "bank_statement_kpis": bank_statement_kpis,
    "credit_report_kpis": credit_report_kpis,
    "identity_doc_kpis": identity_doc_kpis,
    "income_proof_kpis": income_proof_kpis,
    "tax_statement_kpis": tax_statement_kpis,
    "utility_bill_kpis": utility_bill_kpis
}   




@dataclass
class Weights:
    income: float = 0.28
    credit_score: float = 0.23
    delinquency_risk: float = 0.18
    dti: float = 0.17
    liquidity: float = 0.09
    income_consistency: float = 0.03
    employment_stability: float = 0.02
    residency_stability: float = 0.00  # optional

    def normalize(self):
        total = sum(getattr(self, f) for f in self.__dataclass_fields__)
        for f in self.__dataclass_fields__:
            setattr(self, f, getattr(self, f) / total)


def _to_float(x):
    if x is None:
        return None
    try:
        return float(str(x).replace("$", "").replace(",", "").strip())
    except:
        return None


class LoanUnderwritingScorerSimple:

    def __init__(self, weights: Weights | None = None):
        self.w = weights or Weights()
        self.w.normalize()

    # Scoring functions
    def _score_income(self, gmi):
        if gmi is None or gmi <= 0: return None
        if gmi >= 8000: return 100
        if gmi >= 5000: return 80 + (gmi - 5000) * (20/3000)
        if gmi >= 3000: return 60 + (gmi - 3000) * (20/2000)
        if gmi >= 2000: return 40 + (gmi - 2000) * (20/1000)
        return 20

    def _score_credit(self, cs):
        if cs is None: return None
        if cs >= 750: return 100
        if cs >= 700: return 80 + (cs-700)*0.4
        if cs >= 650: return 60 + (cs-650)*0.4
        if cs >= 600: return 40 + (cs-600)*0.4
        return 20

    def _score_dti(self, dti):
        if dti is None: return None
        if dti <= 0.25: return 100
        if dti <= 0.36: return 80
        if dti <= 0.43: return 60
        return 20

    def _score_liquidity(self, balance):
        if balance is None: return None
        if balance >= 5000: return 100
        if balance >= 2500: return 80
        if balance >= 1000: return 60
        if balance >= 0: return 40
        return 20

    def _score_delinquency(self, d30, d60, d90, banks, col):
        score = 100
        score -= min(d30,5)*8
        score -= min(d60,5)*18
        score -= min(d90,5)*28
        score -= min(col,5)*15
        score -= min(banks,2)*50
        return max(0, min(100, score))

    def _score_income_stability(self, flag):
        if not flag: return None
        flag = flag.lower()
        if flag in ("stable", "consistent"): return 100
        if flag in ("variable", "volatile"): return 60
        return 80

    def _score_employment_stability(self, months):
        if months is None: return None
        if months >= 24: return 100
        if months >= 12: return 70
        return 40

    def _score_residency(self, recency_label):
        if not recency_label: return None
        if "recent" in recency_label.lower(): return 100
        return 60

    # Main scoring function
    def score(self, f: Dict[str, Any]) -> Dict[str, Any]:

        gmi = _to_float(f.get("Gross Monthly Income"))
        cs  = _to_float(f.get("credit_score") or f.get("representative_credit_score"))
        dti = _to_float(f.get("debt_to_income_ratio") or f.get("dti"))
        bal = _to_float(f.get("average_monthly_balance"))
        d30 = int(_to_float(f.get("30_day_delinquencies") or 0))
        d60 = int(_to_float(f.get("60_day_delinquencies") or 0))
        d90 = int(_to_float(f.get("90_day_delinquencies") or 0))
        banks = int(_to_float(f.get("bankruptcies") or 0))
        col = int(_to_float(f.get("collections") or 0))
        stab = f.get("stability_flag")
        emp = _to_float(f.get("employment_tenure_months"))
        res = f.get("Billing Recency Check")

        scores = {
            "income_score": self._score_income(gmi),
            "credit_score_score": self._score_credit(cs),
            "delinquency_risk_score": self._score_delinquency(d30, d60, d90, banks, col),
            "dti_score": self._score_dti(dti),
            "liquidity_score": self._score_liquidity(bal),
            "income_consistency_score": self._score_income_stability(stab),
            "employment_stability_score": self._score_employment_stability(emp),
            "residency_stability_score": self._score_residency(res)
        }

        # Weighted average ignoring missing scores
        total_w = 0
        total_s = 0
        for name, score in scores.items():
            if score is not None:
                w = getattr(self.w, name.replace("_score",""))
                total_w += w
                total_s += w * score

        return {
            "sub_scores": scores,
            "final_weighted_score": round(total_s / total_w, 2) if total_w > 0 else None
        }
