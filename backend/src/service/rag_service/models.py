from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, field


@dataclass
class RawDocument:
    case_id: str
    document_type: str
    path: Path
    text: str


@dataclass
class AllDocument:
    case_id: str
    docs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    path: Path | None = None


@dataclass
class DocumentChunk:
    case_id: str
    chunk_id: str
    text: str
    metadata: Dict[str, Any]


@dataclass
class RetrievedChunk:
    chunk: DocumentChunk
    score: float
