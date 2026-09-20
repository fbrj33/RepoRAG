from rag.retriever import CodeRetriever
from rag.keyword_retriever import KeywordRetriever


class HybridRetriever:
    def __init__(
        self,
        semantic_retriever: CodeRetriever,
        keyword_retriever: KeywordRetriever,
    ):
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever

    @staticmethod
    def _get_chunk_id(chunk: dict) -> str:
        """Create a unique identifier for a retrieved chunk."""
        return (
            f"{chunk['file_path']}::{chunk.get('chunk_id', '')}"
        )

    def retrieve(
        self,
        query: str,
        k: int = 5,
        semantic_k: int | None = None,
        keyword_k: int | None = None,
        smantic_k: int | None = None,
    ) -> list[dict]:
        """Retrieve relevant code chunks using both semantic and keyword retrieval."""

        if semantic_k is None:
            semantic_k = smantic_k if smantic_k is not None else k
        if keyword_k is None:
            keyword_k = k

        semantic_results = self.semantic_retriever.retrieve(
            query,
            k=semantic_k,
        )

        keyword_results = self.keyword_retriever.retrieve(
            query,
            k=keyword_k,
        )

        combined = {}
        rrf_k = 60

        for rank, chunk in enumerate(semantic_results, start=1):
            chunk_id = self._get_chunk_id(chunk)

            if chunk_id not in combined:
                combined[chunk_id] = {
                    "chunk": chunk,
                    "rrf_score": 0.0,
                    "semantic_rank": None,
                    "keyword_rank": None,
                }

            combined[chunk_id]["rrf_score"] += 1 / (rrf_k + rank)
            combined[chunk_id]["semantic_rank"] = rank

        for rank, chunk in enumerate(keyword_results, start=1):
            chunk_id = self._get_chunk_id(chunk)

            if chunk_id not in combined:
                combined[chunk_id] = {
                    "chunk": chunk,
                    "rrf_score": 0.0,
                    "semantic_rank": None,
                    "keyword_rank": None,
                }

            combined[chunk_id]["rrf_score"] += 1 / (rrf_k + rank)
            combined[chunk_id]["keyword_rank"] = rank

        ranked_results = sorted(
            combined.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        results = []
        for item in ranked_results[:k]:
            chunk = item["chunk"]
            results.append(
                {
                    **chunk,
                    "rrf_score": item["rrf_score"],
                    "semantic_rank": item["semantic_rank"],
                    "keyword_rank": item["keyword_rank"],
                }
            )

        return results
