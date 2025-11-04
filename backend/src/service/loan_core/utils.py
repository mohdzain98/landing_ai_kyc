import json
from pathlib import Path
from typing import Optional, Dict

from src.service.doc_extractor.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

def get_document_files(document_type: str, base_path: str):
    """
    Reads and returns the markdown, txt, and json file contents 
    for a given document type and base path, with error handling.

    Args:
        document_type (str): Type of document (e.g., 'bank-statements')
        base_path (str): Base directory path

    Returns:
        dict: Dictionary containing file contents (or None if file missing)
    """
    base = Path(base_path) / document_type / "output"
    markdown_path = base / f"{document_type}_parsed.md"
    txt_path = base / f"{document_type}_parsed.txt"
    json_path = base / f"{document_type}.json"

    result = {"markdown": None, "txt": None, "json": None}

    try:
        if markdown_path.exists():
            result["markdown"] = markdown_path.read_text(encoding="utf-8")
        else:
            logger.info(f"⚠️ Markdown file not found: {markdown_path}")

        if txt_path.exists():
            result["txt"] = txt_path.read_text(encoding="utf-8")
        else:
            logger.info(f"⚠️ TXT file not found: {txt_path}")

        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                result["json"] = json.load(f)
        else:
            logger.info(f"⚠️ JSON file not found: {json_path}")

    except Exception as e:
        logger.error(f"❌ Error reading files for '{document_type}': {e}")

    return result



# files = get_document_files(
#     document_type='bank-statements',
#     base_path='/Users/rahulkushwaha/Desktop/kyc_ad/landing_ai_kyc/backend/resources/bc0f8f34-1933-448b-9259-de05b80a0814'
# )

def save_json_to_file( data: dict, base_path: str, document_type: str) -> Optional[str]:
    """Save JSON object to 'base_path/output/{document_type}.json'."""
    try:
        file_path = Path(base_path) /f"{document_type}"/ "output"/ f"{document_type}_kpis.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"JSON saved successfully at {file_path}")
        return str(file_path)
    except Exception as e:
        logger.exception(f"Error saving JSON file: {e}")
        return None
    

def get_document_kpis_files(document_type: str, base_path: str):
    """
    Reads and returns the json file contents 
    for a given document type and base path, with error handling.

    Args:
        document_type (str): Type of document (e.g., 'bank-statements')
        base_path (str): Base directory path

    Returns:
        dict: Dictionary containing file contents (or None if file missing)
    """
    base = Path(base_path) / document_type / "output"
    json_path = base / f"{document_type}_kpis.json"

    result = None
    try:

        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                result = json.load(f)
        else:
            logger.info(f"⚠️ JSON file not found: {json_path}")

    except Exception as e:
        logger.error(f"❌ Error reading files for '{document_type}': {e}")

    return result


