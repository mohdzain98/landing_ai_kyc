import json
from pathlib import Path

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



files = get_document_files(
    document_type='bank-statements',
    base_path='/Users/rahulkushwaha/Desktop/kyc_ad/landing_ai_kyc/backend/resources/bc0f8f34-1933-448b-9259-de05b80a0814'
)


