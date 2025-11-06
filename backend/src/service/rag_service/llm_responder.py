from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from google import genai
from src.service.rag_service.utils import Config, Logger

logger = Logger.get_logger(__name__)


class LLMResponder:
    def __init__(
        self,
        *,
        model: str = "gemini-2.0-flash",
        style: str = "concise",
        max_context_chars: int = 12_000,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.style = style
        self.max_context_chars = max_context_chars
        self.config = Config()
        self.api_key = api_key or self.config.gemini_api_key

        if not self.api_key:
            raise ValueError("Gemini API key is required for LLM responses.")

    def answer(
        self,
        query: str,
        contexts: Iterable[str],
        final_kpis: Optional[Dict[str]] = None,
        final_decision: Optional[Dict[str]] = None,
        *,
        memory: Optional[Iterable[str]] = None,
    ) -> Dict[str, str]:
        stitched = self._build_context(contexts)
        memory_block = self._build_memory(memory)
        instruction = (
            "You are an intelligent retrieval-augmented assistant. "
            "Always speak directly to the user as if the information in the context belongs to them. "
            "Use a natural, second-person tone (use 'you', 'your', etc.), not third-person phrasing. "
            "Use both the provided context and the final KPIs and decision as your main sources of truth. Give priority to the context when answering. If there is less information in the context, rely more with the final KPIs and decision. "
            "If the user greets you (e.g., 'hi', 'hello', 'hey'), respond exactly with:"
            "Hello, how can I help you with your documents?"
            "Otherwise, respond normally to their question."
            "If details are implied, infer them logically from these sources without inventing facts. "
            "If neither the context nor the final KPIs contain enough information, politely say you couldn't find the answer. "
            f"Respond in a single, clear {self.style} paragraph.\n\n"
            "--- CONTEXT START ---\n"
            f"{stitched}\n"
            "--- CONTEXT END ---\n\n"
            "These are the final KPIs and final decision made by the process.\n"
            "--- FINAL KPIs START ---\n"
            f"{final_kpis}\n"
            "--- FINAL KPIs END ---\n\n"
            "--- FINAL DECISION START ---\n"
            f"{final_decision}\n"
            "--- FINAL DECISION END ---\n\n"
        )
        if memory_block:
            instruction += (
                "The following conversation history may contain follow-up details. "
                "Use it only to resolve pronouns or references when the context above is insufficient.\n"
                "--- MEMORY START ---\n"
                f"{memory_block}\n"
                "--- MEMORY END ---\n\n"
            )
        instruction += f"User question: {query}\n"
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model,
            contents=[{"role": "user", "parts": [{"text": instruction}]}],
        )
        answer = (response.text or "").strip()
        logger.info("Generated answer with Gemini model %s", self.model)
        return {"answer": answer, "query": query, "used_context": stitched}

    # ------------------------------------------------------------------ #
    def _build_context(self, contexts: Iterable[str]) -> str:
        bucket: List[str] = []
        total_chars = 0
        for idx, ctx in enumerate(contexts, start=1):
            snippet = ctx.strip()
            if not snippet:
                continue
            block = f"[{idx}]\n{snippet}\n"
            if total_chars + len(block) > self.max_context_chars:
                break
            bucket.append(block)
            total_chars += len(block)
        return "\n".join(bucket)

    def _build_memory(self, memory: Optional[Iterable[str]]) -> str:
        if not memory:
            return ""
        bucket: List[str] = []
        total_chars = 0
        for idx, item in enumerate(memory, start=1):
            snippet = str(item).strip()
            if not snippet:
                continue
            block = f"[{idx}] {snippet}"
            if total_chars + len(block) > self.max_context_chars:
                break
            bucket.append(block)
            total_chars += len(block)
        return "\n".join(bucket)
