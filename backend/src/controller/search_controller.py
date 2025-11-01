from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.search_service.search_doc import search


router = APIRouter()


@router.get("/search-doc", response_model=Response)
async def search_docs(uuid: str):

    search_response = search(uuid)

    if search_response == -1:
        return Response(
            status=404,
            message="Document Search results",
            data={
                "content": "No Data Found",
                "uuid": uuid
            },
            errors="No Data Found",
        )
    else:
        return Response(
            status=200,
            message="Document Search results",
            data={
                "content": search_response,
                "uuid": uuid
            },
            errors=None,
        )
