import hashlib
import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from src.service.rag_service.utils import Logger

logger = Logger.get_logger()


class Faiss:
    def __init__(
        self, index_dir="rag_index", model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        base_dir = Path(__file__).resolve().parent
        self.index_dir = Path(f"{base_dir}/{index_dir}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index_path = self.index_dir / "index.faiss"
        self.meta_path = self.index_dir / "meta.json"
        self.index_dir.mkdir(parents=True, exist_ok=True)

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

    # def save_summary_to_faiss(self, case_id: str, summary_text: str):
    #     vec = self.model.encode([summary_text], normalize_embeddings=True).astype(
    #         "float32"
    #     )
    #     d = vec.shape[1]

    #     index = self._load_or_init_index(d)  # IDMap guaranteed here

    #     # Stable 64-bit ID from case_id
    #     cid = np.int64(
    #         int(hashlib.md5(case_id.encode()).hexdigest()[:16], 16) & ((1 << 63) - 1)
    #     )

    #     # Upsert by ID (remove old, add new)
    #     index.remove_ids(faiss.IDSelectorBatch(np.array([cid], dtype="int64")))
    #     index.add_with_ids(vec, np.array([cid], dtype="int64"))

    #     # Persist index + meta
    #     faiss.write_index(index, str(self.index_path))
    #     meta = self._load_meta()
    #     meta["model_name"] = self.model_name
    #     # meta.setdefault("summaries", {})= summary_text
    #     meta["summaries"] = summary_text
    #     meta["ids"] = int(cid)
    #     self._save_meta(meta)
    #     logger.info(f"✅ Saved {case_id} | total={index.ntotal}")

    # def get_summary_by_case_id(
    #     self,
    #     case_id: str,
    # ) -> Optional[str]:
    #     """
    #     Return the stored raw summary text for a case_id (from meta.json).
    #     """
    #     if not self.index_path.exists() and not self.meta_path.exists():
    #         print(f"No FAISS index found for case_id={case_id}")
    #         return None

    #     index = faiss.read_index(str(self.index_path))
    #     if self.meta_path.exists():
    #         meta = self._load_meta()
    #     return index, meta.get("summaries", {})
