from __future__ import annotations

from typing import Dict, Iterable, List

import faiss
import numpy as np

from src.service.rag_service.core import Faiss
from src.service.rag_service.models import DocumentChunk, RetrievedChunk


class ChunkFaissStore(Faiss):
    """
    Extends the existing Faiss helper to store and retrieve chunk-level embeddings
    for an individual case. Each case receives its own FAISS index directory:

        rag_service/rag_index/<case_id>/

    The parent Faiss class already knows how to manage sentence-transformer
    embeddings and persist the index/metadata. We reuse that functionality while
    expanding the metadata it records so we can map FAISS IDs back to chunk text.
    """

    def __init__(
        self,
        case_id: str,
        *,
        index_root: str = "rag_index",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.case_id = case_id
        super().__init__(index_dir=f"{index_root}/{case_id}", model_name=model_name)

    # --------------------------------------------------------------------- #
    # Public ingestion API
    # --------------------------------------------------------------------- #
    def reset(self) -> None:
        """Remove any previously stored index/metadata for this case."""
        if self.index_path.exists():
            self.index_path.unlink()
        if self.meta_path.exists():
            self.meta_path.unlink()
        # Ensure the directory still exists so future writes succeed.
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def upsert_chunks(self, chunks: Iterable[DocumentChunk]) -> int:
        """
        Encode and persist the supplied chunks. Existing entries for the same
        chunk IDs are replaced. Returns the number of chunks stored.
        """
        chunk_list = list(chunks)
        if not chunk_list:
            return 0

        texts = [chunk.text for chunk in chunk_list]
        embeddings = self.model.encode(texts, normalize_embeddings=True).astype(
            "float32"
        )
        dim = embeddings.shape[1]

        index = self._load_or_init_index(dim)
        meta = self._load_meta()
        meta.setdefault("chunks", {})
        meta.setdefault("id_to_chunk", {})
        meta["model_name"] = self.model_name
        meta["case_id"] = self.case_id

        # Remove any records for this case (fresh rebuild) before re-adding.
        if meta["id_to_chunk"]:
            self._remove_ids(index, meta["id_to_chunk"].keys())
            meta["chunks"].clear()
            meta["id_to_chunk"].clear()

        ids = []
        for chunk in chunk_list:
            raw_id = int(self._caseid_to_int64(f"{chunk.case_id}:{chunk.chunk_id}"))
            ids.append(raw_id)
            meta["id_to_chunk"][str(raw_id)] = chunk.chunk_id
            meta["chunks"][chunk.chunk_id] = {
                "case_id": chunk.case_id,
                "text": chunk.text,
                "metadata": chunk.metadata,
            }

        id_array = np.array(ids, dtype="int64")
        self._remove_ids(index, id_array)
        index.add_with_ids(embeddings, id_array)

        faiss.write_index(index, str(self.index_path))
        self._save_meta(meta)
        return len(chunk_list)

    # --------------------------------------------------------------------- #
    # Retrieval helpers
    # --------------------------------------------------------------------- #
    def similarity_search(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """
        Embed a query, search the per-case index, and return the top matches
        along with their scores and metadata.
        """
        if not self.index_path.exists() or not self.meta_path.exists():
            return []

        meta = self._load_meta()
        id_to_chunk: Dict[str, str] = meta.get("id_to_chunk", {})
        stored_chunks: Dict[str, Dict] = meta.get("chunks", {})
        if not id_to_chunk or not stored_chunks:
            return []

        index = faiss.read_index(str(self.index_path))
        if not isinstance(index, faiss.IndexIDMap):
            index = faiss.IndexIDMap(index)

        vector = self.model.encode([query], normalize_embeddings=True).astype("float32")
        scores, ids = index.search(vector, min(top_k, index.ntotal))
        if ids.size == 0:
            return []

        matches: List[RetrievedChunk] = []
        for raw_id, score in zip(ids[0], scores[0]):
            if raw_id < 0:
                continue
            chunk_id = id_to_chunk.get(str(int(raw_id)))
            if not chunk_id:
                continue
            chunk_info = stored_chunks.get(chunk_id)
            if not chunk_info:
                continue
            doc_chunk = DocumentChunk(
                case_id=chunk_info.get("case_id", self.case_id),
                chunk_id=chunk_id,
                text=chunk_info.get("text", ""),
                metadata=chunk_info.get("metadata", {}),
            )
            matches.append(RetrievedChunk(chunk=doc_chunk, score=float(score)))
        return matches

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _remove_ids(self, index: faiss.IndexIDMap, ids: Iterable[int]) -> None:
        arr = np.fromiter((int(i) for i in ids), dtype="int64", count=-1)
        if arr.size == 0:
            return
        selector = faiss.IDSelectorBatch(arr)
        index.remove_ids(selector)
