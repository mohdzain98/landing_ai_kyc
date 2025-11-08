from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from google import genai
from langchain_aws import ChatBedrock

from src.service.rag_service.utils import Config, Logger

logger = Logger.get_logger(__name__)


class LLMResponder:

    def __init__(
        self,
        *,
        model: str = "amazon.titan-text-express-v1",
        style: str = "concise",
        max_context_chars: int = 12000,
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
            "You are an intelligent retrieval-augmented assistant."
            "STYLE & TONE"
            "- Speak directly to the user as if the information in the context belongs to them (use “you”, “your”)."
            f"- Respond in a single, clear {self.style} paragraph."
            "GREETING OVERRIDE"
            "- If the user greets you (e.g., 'hi', 'hello', 'hey'), respond EXACTLY with:"
            "Hello, how can I help you with your documents?"
            "- When you do this, do not add any other text."
            "SOURCES & PRIORITY"
            "- You have three sources: CONTEXT, FINAL KPIs, FINAL DECISION."
            "- Primary: Use CONTEXT as the first source of truth."
            "- If the user’s question is about a final outcome, recommendation, approval/rejection, or “what should I do?”, use the FINAL DECISION (and KPIs as needed)."
            "- If CONTEXT lacks relevant details, rely on FINAL KPIs and FINAL DECISION."
            "- Never invent facts beyond these sources."
            "OUTPUT CONTENT RULES"
            "- Answer the question using the prioritized sources above."
            "- If neither CONTEXT nor FINAL KPIs/DECISION contain enough info to answer, say you couldn’t find the answer and suggest what is missing; still provide any available KPI highlights if relevant."
            "- Keep the whole response to one paragraph\n"
            "--- CONTEXT START ---\n\n"
            f"context:\n{stitched}\n"
            "--- CONTEXT END ---\n\n"
            "--- FINAL KPIs START ---\n"
            f"{final_kpis}\n\n"
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
        # client = genai.Client(api_key=self.api_key)
        # response = client.models.generate_content(
        #     model=self.model,
        #     contents=[{"role": "user", "parts": [{"text": instruction}]}],
        # )
        llm = ChatBedrock(
            model_id="amazon.titan-text-express-v1",
            region="us-east-1",
            aws_access_key_id=self.config.aws_access_key,
            aws_secret_access_key=self.config.aws_secret_key,
        )
        response = llm.invoke(instruction)
        answer = (response.content or "").strip()
        logger.info("Generated answer with Bedrock model %s", self.model)
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
