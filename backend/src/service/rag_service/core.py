from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings

from src.service.rag_service.utils import Logger

DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

logger = Logger.get_logger(__name__)


@lru_cache(maxsize=4)
def get_embeddings(model_name: str = DEFAULT_EMBED_MODEL) -> HuggingFaceEmbeddings:
    """
    Return a cached HuggingFace embeddings model. Cached to avoid re-loading
    sentence-transformer weights for every request.
    """
    logger.info("Loaded sentence-transformer model '%s'", model_name)
    return HuggingFaceEmbeddings(model_name=model_name)


def index_dir_for(case_id: str, index_root: str = "rag_index") -> Path:
    base_dir = Path(__file__).resolve().parent
    target = base_dir / index_root / case_id
    target.mkdir(parents=True, exist_ok=True)
    return target
