import hashlib
import json
from pathlib import Path
from typing import Iterable, List

import faiss
import numpy as np

from src.service.rag_service.utils import Logger

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore[assignment]

logger = Logger.get_logger(__name__)


class _FallbackEncoder:
    """
    Lightweight deterministic embedding generator used when
    sentence-transformers is unavailable or cannot download models.
    Produces 256-dimensional embeddings by hashing byte values.
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def encode(
        self, texts: Iterable[str], normalize_embeddings: bool = True
    ) -> np.ndarray:
        vectors: List[np.ndarray] = []
        for text in texts:
            vec = np.zeros(self.dim, dtype="float32")
            if text:
                data = text.encode("utf-8", errors="ignore")
                for idx, value in enumerate(data):
                    vec[idx % self.dim] += float(value)
            if normalize_embeddings:
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec /= norm
            vectors.append(vec)
        if not vectors:
            vectors.append(np.zeros(self.dim, dtype="float32"))
        return np.stack(vectors, axis=0)


class Faiss:
    def __init__(
        self, index_dir="rag_index", model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        base_dir = Path(__file__).resolve().parent
        self.index_dir = Path(f"{base_dir}/{index_dir}")
        self.model_name = model_name
        self.model = self._load_model(model_name)
        self.index_path = self.index_dir / "index.faiss"
        self.meta_path = self.index_dir / "meta.json"
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def _load_model(self, model_name: str):
        if SentenceTransformer is None:
            logger.warning(
                "sentence-transformers not available; using fallback hash encoder."
            )
            return _FallbackEncoder()
        try:
            return SentenceTransformer(model_name)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning(
                "Failed to load '%s' model (%s). Falling back to hash encoder.",
                model_name,
                exc,
            )
            return _FallbackEncoder()

    def _caseid_to_int64(self, case_id: str) -> np.int64:
        h = hashlib.md5(case_id.encode("utf-8")).hexdigest()
        return np.int64(int(h[:16], 16) & ((1 << 63) - 1))

    def _load_or_init_index(self, dim: int):
        # If the file exists but is 0 bytes, delete it (corrupt/empty file)
        if self.index_path.exists() and self.index_path.stat().st_size == 0:
            self.index_path.unlink()

        if not self.index_path.exists():
            # Fresh: build ID-mapped index FIRST, then add_with_ids later
            base = faiss.IndexFlatIP(dim)
            return faiss.IndexIDMap(base)

        base = faiss.read_index(str(self.index_path))
        # If it’s already an IDMap, just reuse it
        if isinstance(base, faiss.IndexIDMap):
            return base

        # Plain index on disk; if empty, we can wrap. If not, reset to a fresh IDMap.
        if base.ntotal == 0:
            return faiss.IndexIDMap(base)

        # Non-empty plain index -> cannot wrap. Reset (warn once).
        print("⚠️ Non-empty non-ID index found; recreating fresh ID-mapped index.")
        base = faiss.IndexFlatIP(dim)
        return faiss.IndexIDMap(base)

    def _load_meta(self):
        if self.meta_path.exists():
            return json.loads(self.meta_path.read_text("utf-8"))
        return {"model_name": self.model_name, "summaries": {}, "ids": {}}

    def _save_meta(self, meta):
        logger.info(f"meta.json saved at {self.meta_path}")
        self.meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
