from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.search_service.search_doc import search


router = APIRouter()


@router.get("/search-doc", response_model=Response)
async def search_docs(uuid: str, folder_type: str):
    return Response(
        status=200,
        message="Document Evaluation done",
        data={
            "content": search(uuid, folder_type),
            "uuid": uuid
        },
        errors=None,
    )
