import os
import json
from uuid import uuid4
from pathlib import Path
from typing import Dict, Optional, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile


async def persist_file_in_local(metadata, identity_documents, bank_statements, tax_statements, credit_reports, income_proof,
                          utility_bills):

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
        case_id = str(uuid4())

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
            filename = sanitize_filename(upload_file.filename)
            destination = category_dir / filename
            await save_upload_file(upload_file, destination)
            saved_files.append(
                {
                    "category": category,
                    "folder": str(category_dir),
                    "filename": filename,
                    "path": str(destination),
                }
            )

    return case_id


async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
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


def sanitize_filename(filename: str) -> str:
    return Path(filename).name
