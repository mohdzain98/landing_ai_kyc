import json

class DecisionEngine:
    def __init__(self):
        """Initialize the DecisionEngine."""
        pass

    def make_decision(self, loan_metrics={}, final_score={}, fraud_result={},text_fraud_result={}):
        """
        Combine outputs from all modules to decide loan approval status.

        Parameters:
        -----------
        loan_metrics : dict
            Contains metrics or indicators related to the loan applicant (optional).

        final_score : dict
            Contains the final weighted score or credit score from prior evaluations.

        fraud_result : dict
            Contains the result of document authenticity checks (e.g., is_authentic flag).

        text_fraud_result : dict
            Contains the result of document consistency.

        Returns:
        --------
        dict
            Decision summary with loan status, reason, and score.
        """
        # ===========================
        # 🔹 Step 1: Identity Fraud Check
        # ===========================
        is_authentic = fraud_result['is_authentic']
        is_text_fraud  = text_fraud_result['type']

        # ===========================
        # 🔹 Step 2: Proceed if documents are authentic
        # ===========================
        if is_authentic:
            # Default decision setup
            decision = {
                "status": "manual_review",
                "reason": "Unable to determine automatically",
                "score": final_score.get("final_weighted_score", None),
            }
            # ===========================
            # 🔹 Step 3: Evaluate text fraud
            # ===========================
            if is_text_fraud == "Authentic":

                # ===========================
                # 🔹 Step 5: Evaluate based on credit/weighted score
                # ===========================
                score = final_score.get("final_weighted_score", 0)

                # High score → Approved
                if score >= 60:
                    decision["status"] = "approved"
                    decision["reason"] = "Strong financial and credit indicators"

                # Medium score → Manual review
                elif 40 <= score < 60:
                    decision["status"] = "manual_review"
                    decision["reason"] = "Borderline score; manual verification needed"

                # Low score → Rejected
                else:
                    decision["status"] = "rejected"
                    decision["reason"] = "Low creditworthiness"

                return decision
            else:
                return {
                "status": "manual_review",
                "reason": "Douments are not authentic",
                "score": 0,
            }


        # ===========================
        # 🔹 Step 6: Reject if documents are fraudulent
        # ===========================
        else:
            return {
                "status": "Rejected",
                "reason": "Douments are not authentic",
                "score": 0,
            }
