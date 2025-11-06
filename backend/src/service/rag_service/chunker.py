from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

from src.service.rag_service.models import DocumentChunk, RawDocument


@dataclass
class ChunkingConfig:
    chunk_size: int = 800
    chunk_overlap: int = 160


class TextChunker:
    """
    Lightweight whitespace-normalising chunker. Designed to work with the
    `RawDocument` records produced by `CaseDocumentLoader`.
    """

    def __init__(self, *, config: ChunkingConfig | None = None) -> None:
        self.config = config or ChunkingConfig()
        if self.config.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if self.config.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if self.config.chunk_overlap >= self.config.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

    def chunk_documents(self, documents: Iterable[RawDocument]) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        for document in documents:
            chunks.extend(self._chunk_single_document(document))
        return chunks

    # ------------------------------------------------------------------ #
    def _chunk_single_document(self, document: RawDocument) -> List[DocumentChunk]:
        cleaned = self._normalise_text(document.text)
        if not cleaned:
            return []

        results: List[DocumentChunk] = []
        cursor = 0
        index = 0
        size = self.config.chunk_size
        overlap = self.config.chunk_overlap

        while cursor < len(cleaned):
            end = min(len(cleaned), cursor + size)
            snippet = cleaned[cursor:end].strip()
            if snippet:
                chunk_id = f"{document.document_type}-{index}"
                metadata = {
                    "document_type": document.document_type,
                    "source": str(document.path),
                    "chunk_index": index,
                }
                results.append(
                    DocumentChunk(
                        case_id=document.case_id,
                        chunk_id=chunk_id,
                        text=snippet,
                        metadata=metadata,
                    )
                )
            index += 1
            if end >= len(cleaned):
                break
            cursor = max(0, end - overlap)
        return results

    def _normalise_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()
