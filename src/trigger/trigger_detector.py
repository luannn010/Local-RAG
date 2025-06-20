# src/trigger_detector.py

from typing import List
import numpy as np

class TriggerDetector:
    # Define phrases that indicate a query is about the knowledge base
    KEYWORDS: List[str] = [
        "note", "document", "file", "knowledge", "information", "tell me about", "from vault", "about note"
    ]

    @staticmethod
    def should_trigger(query: str) -> bool:
        """
        Returns True if any trigger keyword is found in the query.
        """
        lowered = query.lower()
        return any(kw in lowered for kw in TriggerDetector.KEYWORDS)

    @staticmethod
    def is_semantic_trigger(query: str, embedder, reference_phrases: List[str], threshold: float = 0.8) -> bool:
        """
        Optional: Semantic trigger using cosine similarity against reference phrases.
        """
        query_vec = embedder.embed_query(query)
        for phrase in reference_phrases:
            ref_vec = embedder.embed_query(phrase)
            sim = TriggerDetector.cosine_similarity(query_vec, ref_vec)
            if sim >= threshold:
                return True
        return False

    @staticmethod
    def cosine_similarity(vec1, vec2):
        vec1, vec2 = np.array(vec1), np.array(vec2)
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))