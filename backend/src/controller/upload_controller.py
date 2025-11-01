from typing import List, Optional
from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.utils.upload_file_utils import persist_file_in_local
# from src.service.main import process_documents

router = APIRouter()


@router.post("/bank_statement", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    bank_statements: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, bank_statements, "bank_statements")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )


@router.post("/identity_document", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    identity_documents: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, identity_documents, "identity_documents")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )


@router.post("/credit_report", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    credit_reports: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, credit_reports, "credit_reports")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )


@router.post("/income_proof", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    income_proof: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, income_proof, "income_proof")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )


@router.post("/tax_statement", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    tax_statements: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, tax_statements, "tax_statements")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )


@router.post("/utility_bills", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    utility_bills: Optional[List[UploadFile]] = File(None)
) -> Response:

    folder_id = await persist_file_in_local(metadata, utility_bills, "utility_bills")

    # process_documents(folder_id)

    return Response(
        status=200,
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id,
            "content": None
        },
        errors=None,
    )

