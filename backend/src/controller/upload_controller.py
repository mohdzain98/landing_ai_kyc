import json
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.model.Response import Response


router = APIRouter()


async def _save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Persist an UploadFile to disk in chunks to avoid high memory usage."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        await upload_file.seek(0)
        with destination.open("wb") as buffer:
            while True:
                chunk = await upload_file.read(1024 * 1024)
                if not chunk:
                    break
                buffer.write(chunk)
    finally:
        await upload_file.close()


def _sanitize_filename(filename: str) -> str:
    return Path(filename).name


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
    category_map: Dict[str, Optional[List[UploadFile]]] = {
        "identity_documents": identity_documents,
        "bank_statements": bank_statements,
        "tax_statements": tax_statements,
        "credit_reports": credit_reports,
        "income_proof": income_proof,
        "utility_bills": utility_bills,
    }

    if not any(files for files in category_map.values() if files):
        raise HTTPException(status_code=400, detail="No documents received to upload.")

    case_id = None
    if metadata:
        try:
            meta = json.loads(metadata)
            case_id = meta.get("caseId") or meta.get("userId")
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=400, detail=f"Invalid metadata payload: {exc}"
            ) from exc

    if not case_id:
        case_id = str(uuid.uuid4())

    base_dir = Path(os.getcwd()) / "resources" / case_id
    base_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for category, files in category_map.items():
        if not files:
            continue
        folder_name = category.replace("_", "-")
        category_dir = base_dir / folder_name
        for upload_file in files:
            if not upload_file.filename:
                continue
            filename = _sanitize_filename(upload_file.filename)
            destination = category_dir / filename
            await _save_upload_file(upload_file, destination)
            saved_files.append(
                {
                    "category": category,
                    "folder": str(category_dir),
                    "filename": filename,
                    "path": str(destination),
                }
            )

    return Response(
        status="success",
        message="Documents uploaded successfully.",
        data={
            "caseId": case_id,
            "savedFiles": saved_files,
        },
        errors=None,
    )


@router.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}
