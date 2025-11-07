from pathlib import Path
from src.service.loan_core.utils import (
    get_document_kpis_files,
    save_responses_to_folder,
)
from src.service.loan_core.loan_metrics import LoanUnderwritingScorerSimple
from src.service.loan_core.decision import DecisionEngine
from src.service.doc_extractor.logger import get_logger
from src.service.rag_service.agent import RAGAgent
from src.service.loan_core.fraud_engine import FraudDetectionEngine

# Initialize logger for this module
logger = get_logger(__name__)

loan_metrics = LoanUnderwritingScorerSimple()
decision_engine = DecisionEngine()
fraud_engine  = FraudDetectionEngine()


def evaluate(folder_id):
    base_path = str((Path(__file__).parent.parent / "resources" / folder_id).resolve())
    base_path = base_path.replace("/src/service", "")

    bank_statements = get_document_kpis_files("bank-statements", base_path)
    logger.info(f"The bank statement is  {bank_statements }")
    identity_documents = get_document_kpis_files("identity-documents", base_path)
    credit_reports = get_document_kpis_files("credit-reports", base_path)
    income_proof = get_document_kpis_files("income-proof", base_path)
    tax_statements = get_document_kpis_files("tax-statements", base_path)
    utility_bills = get_document_kpis_files("utility-bills", base_path)

    # --- Combine all safely ---
    combined_flat = {
        **credit_reports,
        **bank_statements,
        **identity_documents,
        **income_proof,
        **tax_statements,
        **utility_bills,
    }
    logger.info(f"The combined kpis dict is- {combined_flat}")
    response_dict = loan_metrics.score(combined_flat)
    final_descision = decision_engine.make_decision(final_score=response_dict)
    save_responses_to_folder(response_dict, final_descision, base_path)
    fraud_engine.save_fraud_summary(base_path )

    ## Build RAG index after evaluation
    agent = RAGAgent(case_id=folder_id)
    try:
        agent.ingest()
    except Exception as e:
        logger.error(f"Error during RAG ingestion: {e}")

    return str(final_descision["status"])
