import backend.src.service.utils

class KPIService:
    def __init__(self):
        pass

    def calculate(self, docs):
        per_doc_results = []
        for doc in docs:
            if doc['doc_id']=="doc_1":
                bank_statement_kpi.calculate_bank_kpis(doc['bank_statement'])
            # Add other document types KPI calculations here
            elif doc['doc_id']=="doc_2":
                credit_card_kpi.calculate_credit_card_kpis(doc['credit_card'])
            elif doc['doc_id']=="doc_3":
                loan_kpi.calculate_loan_kpis(doc['loan'])

        # Return JSON (dict)
        return {
            "per_document": per_doc_results,
            "aggregate": {
                # Aggregate KPIs across documents if needed
            }
        }
