from sentence_transformers import CrossEncoder


class CodeReranker:
    """Rerank repository chunks using a cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    @staticmethod
    def _build_candidate_text(
        chunk: dict,
    ) -> str:
        """Build metadata-rich text for reranking."""

        file_path = chunk.get("file_path", "")
        chunk_type = chunk.get("type", "")
        name = chunk.get("name") or "N/A"
        start_line = chunk.get("start_line", -1)
        end_line = chunk.get("end_line", -1)
        content = chunk.get("content", "")

        if start_line != -1:
            location = (
                f"{file_path}:{start_line}-{end_line}"
            )
        else:
            location = file_path

        return f"""
File: {file_path}
Location: {location}
Type: {chunk_type}
Name: {name}

Code:
{content}
""".strip()

    def rerank(
        self,
        query: str,
        chunks: list[dict],
        top_k: int = 3,
    ) -> list[dict]:
        """Rerank candidate chunks according to query relevance."""

        if not chunks:
            return []

        candidate_texts = [
            self._build_candidate_text(chunk)
            for chunk in chunks
        ]

        pairs = [
            (query, candidate)
            for candidate in candidate_texts
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