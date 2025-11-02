from fastapi import Form, File, UploadFile, APIRouter

from src.model.Response import Response
from src.service.evaluator_service.evaluator import evaluate


router = APIRouter()


@router.get("/evaluate-doc", response_model=Response)
async def evaluate_docs(uuid: str):
    return Response(
        status=200,
        message="Document Evaluation done",
        data={
            "content": evaluate(uuid),
            "uuid": uuid
        },
        errors=None,
    )
