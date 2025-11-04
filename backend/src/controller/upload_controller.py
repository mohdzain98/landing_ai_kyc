from typing import List, Optional
from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.utils.upload_file_utils import persist_file_in_local
from src.service.summariser_module.get_summary import get_markdown, get_document_data
from src.service.main import process_documents
from src.service.loan_core.utils import get_document_files,save_json_to_file,get_document_kpis_files
from src.service.loan_core.document_kpi_logic.bank_statement_kpi import BankStatementKPIs
from src.service.loan_core.document_kpi_logic.credit_report_kpi import CreditReportKPIs
from src.service.loan_core.document_kpi_logic.salary_kpi import PaystubSimpleKPIs
from src.service.loan_core.document_kpi_logic.tax_statement_1040_kpi import IncomeKPI
from src.service.loan_core.document_kpi_logic.utility_bill_kpi import UtilityKPI
from src.service.loan_core.document_kpi_logic.identity_verification_kpi import calculate_identity_verification_kpis

router = APIRouter()
bankstatement_kpi = BankStatementKPIs()
creditreportkpis  = CreditReportKPIs()
salaryslipkpis = PaystubSimpleKPIs()
incomekpis = IncomeKPI()
utilitykpis  = UtilityKPI()


@router.post("/bank_statement", response_model=Response)
async def upload_bank_statement(
    metadata: Optional[str] = Form(None),
    bank_statements: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, bank_statements, "bank_statements")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    bank_statement_kpis = bankstatement_kpi.calculate(statement_json)
    save_json_to_file(bank_statement_kpis,base_path,document_type)

    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    
    markdown = get_document_data(folder_id, folder_name)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )


@router.post("/identity_document", response_model=Response)
async def upload_identity_document(
    metadata: Optional[str] = Form(None),
    identity_documents: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, identity_documents, "identity_documents")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    identity_kpis = calculate_identity_verification_kpis(statement_json)
    save_json_to_file(identity_kpis,base_path,document_type)

    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_document_data(folder_id, folder_name)
    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )


@router.post("/credit_report", response_model=Response)
async def upload_credit_report(
    metadata: Optional[str] = Form(None),
    credit_reports: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, credit_reports, "credit_reports")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"

    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    credit_kpis = creditreportkpis.calculate(statement_json)
    save_json_to_file(credit_kpis,base_path,document_type)
    markdown = get_document_data(folder_id, folder_name)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )


@router.post("/income_proof", response_model=Response)
async def upload_income_proof(
    metadata: Optional[str] = Form(None),
    income_proof: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, income_proof, "income_proof")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    salary_kpis = salaryslipkpis.calculate(statement_json)
    save_json_to_file(salary_kpis ,base_path,document_type)
    markdown = get_document_data(folder_id, folder_name)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )


@router.post("/tax_statement", response_model=Response)
async def upload_tax_statement(
    metadata: Optional[str] = Form(None),
    tax_statements: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, tax_statements, "tax_statements")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    income_kpis = incomekpis.calculate(statement_json)
    save_json_to_file(income_kpis ,base_path,document_type)
    markdown = get_document_data(folder_id, folder_name)


    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )


@router.post("/utility_bill", response_model=Response)
async def upload_utility_bill(
    metadata: Optional[str] = Form(None),
    utility_bills: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, utility_bills, "utility_bills")
    result, folder_id, document_type, base_path = process_documents(folder_id, folder_name)
    # folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    files = get_document_files(
                                document_type=document_type,
                                base_path=base_path
                                )
    statement_json = files['json']
    utility_kpis = utilitykpis.calculate(statement_json)
    save_json_to_file(utility_kpis ,base_path,document_type)
    markdown = get_document_data(folder_id, folder_name)


    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )

