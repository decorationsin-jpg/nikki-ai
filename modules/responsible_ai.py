"""
Nikki Responsible AI & RAG Fact-Checking Engine.
Implements:
1. RAG (Retrieval-Augmented Generation) over local memory & web search
2. Source Citations
3. Confidence Indicators & Thresholding
4. Fact Verification & Anti-Hallucination Guardrails
5. Structured Outputs & "I don't have enough information" Fallback
"""
import json
import re
from typing import Dict, Any, List
from pathlib import Path
from modules.web_search import FreeWebSearch
from modules.memory_engine import MemoryEngine

class ResponsibleAIEngine:
    """
    Responsible AI Engine implementing RAG, Citations, Confidence Scoring, and Anti-Hallucination.
    """

    def __init__(self, confidence_threshold: float = 0.65):
        self.web = FreeWebSearch()
        self.memory = MemoryEngine()
        self.confidence_threshold = confidence_threshold

    def rag_query(self, query: str) -> Dict[str, Any]:
        """
        Executes Retrieval-Augmented Generation (RAG) to fetch ground-truth facts
        from local memory databases and web search before forming a verified answer.
        """
        retrieved_sources = []
        context_passages = []

        # Step 1: Retrieve from Local User Teachings Memory
        teachings = self.memory.load_teachings()
        facts = teachings.get("user_facts", {})
        query_lower = query.lower()

        for k, v in facts.items():
            if k.lower() in query_lower:
                context_passages.append(f"User Fact ({k}): {v}")
                retrieved_sources.append(f"local_memory:user_teachings.json ({k})")

        # Step 2: Retrieve from Web Search if needed
        if not context_passages:
            try:
                search_results = self.web.search(query, max_results=3)
                if isinstance(search_results, list) and len(search_results) > 0:
                    for item in search_results:
                        snippet = item.get("snippet", "")
                        url = item.get("href", item.get("link", "web_search"))
                        if snippet:
                            context_passages.append(snippet)
                            retrieved_sources.append(url)
            except Exception:
                pass

        # Step 3: Compute Confidence Score & Anti-Hallucination Guardrail
        confidence = self._compute_confidence(query, context_passages)

        # Step 4: Evaluate against Confidence Threshold
        if confidence < self.confidence_threshold:
            return {
                "answer": "I don't have enough information to answer that accurately without inventing facts.",
                "confidence_score": f"{int(confidence * 100)}%",
                "is_verified": False,
                "citations": [],
                "structured_output": {
                    "status": "insufficient_information",
                    "reason": "Retrieved context confidence is below responsible AI threshold."
                }
            }

        # Step 5: Format Verified Structured Answer with Citations
        raw_answer = " ".join(context_passages[:2])
        formatted_answer = f"{raw_answer}\n\n📌 **Source Citations**:\n" + "\n".join([f"- [{src}]" for src in set(retrieved_sources)])

        return {
            "answer": formatted_answer,
            "confidence_score": f"{int(confidence * 100)}%",
            "is_verified": True,
            "citations": list(set(retrieved_sources)),
            "structured_output": {
                "status": "verified",
                "query": query,
                "retrieved_count": len(context_passages),
                "confidence": confidence
            }
        }

    def _compute_confidence(self, query: str, passages: List[str]) -> float:
        """Computes a factual confidence score between 0.0 and 1.0."""
        if not passages:
            return 0.20  # Low confidence if zero context retrieved

        # Check term overlap
        words = [w for w in re.findall(r'\w+', query.lower()) if len(w) > 3]
        if not words:
            return 0.70

        total_passages_text = " ".join(passages).lower()
        matches = sum(1 for w in words if w in total_passages_text)

        overlap_ratio = matches / len(words)
        if overlap_ratio >= 0.6:
            return 0.90  # High confidence
        elif overlap_ratio >= 0.3:
            return 0.70  # Medium confidence
        else:
            return 0.40  # Low confidence
