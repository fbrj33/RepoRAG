from sentence_transformers import CrossEncoder


class CodeReranker:
    """Rerank retrieved repository chunks using a cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: list[dict],
        top_k: int = 3,
    ) -> list[dict]:
        """Rerank candidate chunks according to query relevance."""

        if not chunks:
            return []

        pairs = [
            (query, chunk["content"])
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        ranked_chunks = []

        for chunk, score in zip(chunks, scores):
            ranked_chunks.append(
                {
                    **chunk,
                    "rerank_score": float(score),
                }
            )

        ranked_chunks.sort(
            key=lambda chunk: chunk["rerank_score"],
            reverse=True,
        )

        return ranked_chunks[:top_k]