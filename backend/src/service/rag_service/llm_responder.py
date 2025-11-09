from __future__ import annotations

from typing import Dict, Iterable, List, Optional

# from google import genai
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.service.rag_service.utils import Config, Logger
from src.service.rag_service.main import KPIReferenceLoader

logger = Logger.get_logger(__name__)


class LLMResponder:

    def __init__(
        self,
        *,
        model: str = "amazon.nova-pro-v1:0",
        style: str = "concise",
        max_context_chars: int = 12000,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.style = style
        self.max_context_chars = max_context_chars
        self.config = Config()
        self.kpis = KPIReferenceLoader()
        # self.api_key = api_key or self.config.gemini_api_key

        # if not self.api_key:
        # raise ValueError("Gemini API key is required for LLM responses.")

    def answer(
        self,
        query: str,
        contexts: Iterable[str],
        final_kpis: Optional[Dict[str]] = None,
        final_decision: Optional[Dict[str]] = None,
        kpi_definitions: Optional[Dict[str]] = None,
        *,
        memory: Optional[Iterable[str]] = None,
    ) -> Dict[str, str]:
        stitched = self._build_context(contexts)
        memory_block = self._build_memory(memory)
        intent = self.kpis.detect_intents(question=query)
        logger.info(intent)
        if intent["decision_intent"]:
            stitched += "\n\n--- FINAL DECISION ---\n" + str(final_decision)
        if intent["kpi_intent"]:
            stitched += "\n\n--- Kpis Definitions ---\n" + str(kpi_definitions)
        system_template = """You are an intelligent retrieval-augmented assistant.
        Use ONLY the information in CONTEXT to answer.
        Use MEMORY only to resolve pronouns/references; do not add new facts from memory.
        If the answer is not present in CONTEXT, reply exactly:
        I couldn't find that information in the provided documents.
        Never give generic reasons or background explanations. Respond in one concise paragraph.

        GREETING OVERRIDE:
        If the user greets you (e.g., "hi", "hello", "hey"), respond EXACTLY:
        Hello, how can I help you with your documents?
        Do not add any other text.
        """
        user_template = """--- CONTEXT START ---
        {context}
        --- CONTEXT END ---

        --- MEMORY (use only for resolving references) ---
        {memory}

        User question: {question}
        """
        # client = genai.Client(api_key=self.api_key)
        # response = client.models.generate_content(
        #     model=self.model,
        #     contents=[{"role": "user", "parts": [{"text": instruction}]}],
        # )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                ("user", user_template),
            ]
        )
        llm = ChatBedrock(
            model_id=self.model,
            region="us-east-1",
            aws_access_key_id=self.config.aws_access_key,
            aws_secret_access_key=self.config.aws_secret_key,
            temperature=0.3,
        )
        chain = prompt | llm | StrOutputParser()
        variables = {
            "context": stitched,
            "memory": memory_block,
            "question": query,
        }
        answer = chain.invoke(variables)
        # response = llm.invoke(instruction)
        # answer = (response.content or "").strip()
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
