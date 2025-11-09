import json

class DecisionEngine:
    def __init__(self):
        pass

    def make_decision(self, loan_metrics={}, final_score={}, fraud_result={}):
        """
        Combine outputs from all modules to decide loan approval status.
        """
        # Identity Farud Check
        is_authentic  = fraud_result['is_authentic']

        if is_authentic:
            # Default decision
            decision = {
                "status": "manual_review",
                "reason": "Unable to determine automatically",
                "score": final_score.get("final_weighted_score", None),
            }

            # # 1. Hard rejection check
            # if hard_rules.get("rejected", False):
            #     decision["status"] = "rejected"
            #     decision["reason"] = hard_rules.get("reason", "Hard rule triggered")
            #     return decision

            # # 2. Fraud detection threshold
            # if fraud_result.get("fraud_score", 0) > 0.8:
            #     decision["status"] = "rejected"
            #     decision["reason"] = "High fraud risk detected"
            #     return decision

            # 3. Credit score or weighted score
            score = final_score.get("final_weighted_score", 0)
            if score >= 60:
                decision["status"] = "approved"
                decision["reason"] = "Strong financial and credit indicators"
            elif 40 <= score < 60:
                decision["status"] = "manual_review"
                decision["reason"] = "Borderline score; manual verification needed"
            else:
                decision["status"] = "rejected"
                decision["reason"] = "Low creditworthiness"

            return decision
        else:
            return  {
                "status": "Rejected",
                "reason": "Douments are not authentic",
                "score": 0,
            }


# if __name__ == "__main__":
#     # Mock input
#     loan_metrics = {"dti_ratio": 0.3, "loan_to_income": 0.25}
#     kpis = {"avg_balance": 20000, "salary_stability": 0.9}
#     final_score = {"score": 720}
#     fraud_result = {"fraud_score": 0.2}
#     hard_rules = {"rejected": False}

#     {'sub_scores': {'income_score': 84.66666666666667,
#   'credit_score_score': 43.6,
#   'delinquency_risk_score': 100,
#   'dti_score': None,
#   'liquidity_score': 20,
#   'income_consistency_score': 100,
#   'employment_stability_score': None,
#   'residency_stability_score': 60},
#  'final_weighted_score': 69.8}

#     engine = DecisionEngine()
#     output = engine.make_decision(loan_metrics, kpis, final_score, fraud_result, hard_rules)
#     print(json.dumps(output, indent=4))
