from .loan_metrics import LoanMetricsCalculator
from .kpi_service import KPIService
from .final_score import FinalScoreCalculator
from .fraud_detection import FraudDetectionEngine
from .hard_rules import HardRejectionEngine
from .decision import DecisionEngine

class UnderwritingPipeline:
    def __init__(self, config_paths):
        self.loan_metrics_calc = LoanMetricsCalculator()
        self.kpi_service = KPIService()
        self.final_score_calc = FinalScoreCalculator(config_paths["weights"])
        self.fraud_engine = FraudDetectionEngine(config_paths["fraud_rules"])
        self.hard_rule_engine = HardRejectionEngine(config_paths["hard_rules"])
        self.decision_engine = DecisionEngine()

    def run(self, input_data):
        loan_metrics = self.loan_metrics_calc.calculate(input_data)
        kpis = self.kpi_service.calculate(input_data)
        final_score = self.final_score_calc.calculate(loan_metrics, kpis)
        fraud_result = self.fraud_engine.evaluate(input_data)
        hard_rules = self.hard_rule_engine.check(input_data)
        decision = self.decision_engine.make_decision(
            loan_metrics, kpis, final_score, fraud_result, hard_rules
        )

        return {
            "loan_metrics": loan_metrics,
            "kpis": kpis,
            "final_score": final_score,
            "fraud_result": fraud_result,
            "hard_rules": hard_rules,
            "decision": decision
        }
