from typing import List, Optional
from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.utils.upload_file_utils import persist_file_in_local
from src.service.extract_utils.document_data_extractor import extract

router = APIRouter()


@router.post("/docs", response_model=Response)
async def upload_documents(
    metadata: Optional[str] = Form(None),
    identity_documents: Optional[List[UploadFile]] = File(None),
    bank_statements: Optional[List[UploadFile]] = File(None),
    tax_statements: Optional[List[UploadFile]] = File(None),
    credit_reports: Optional[List[UploadFile]] = File(None),
    income_proof: Optional[List[UploadFile]] = File(None),
    utility_bills: Optional[List[UploadFile]] = File(None),
) -> Response:

    folder_id = await persist_file_in_local(metadata, identity_documents, bank_statements, tax_statements, credit_reports,
                                          income_proof, utility_bills)

    extract(folder_id)

    return Response(
        status="success",
        message="Documents uploaded successfully.",
        data={
            "folderId": folder_id
        },
        errors=None,
    )
