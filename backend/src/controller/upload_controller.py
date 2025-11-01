from typing import List, Optional
from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.utils.upload_file_utils import persist_file_in_local
from src.service.summariser_module.get_summary import get_markdown
# from src.service.main import process_documents

router = APIRouter()


@router.post("/bank_statement", response_model=Response)
async def upload_bank_statement(
    metadata: Optional[str] = Form(None),
    bank_statements: Optional[UploadFile] = File(None)
) -> Response:

    folder_id, folder_name = await persist_file_in_local(metadata, bank_statements, "bank_statements")
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

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
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

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
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

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
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

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
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

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
    # process_documents(folder_id, folder_name)
    folder_id = "bc0f8f34-1933-448b-9259-de05b80a0814"
    markdown = get_markdown(folder_id, folder_name)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": markdown
        },
        errors=None,
    )

