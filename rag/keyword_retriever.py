import re

from rank_bm25 import BM25Okapi


class KeywordRetriever:
    """Retrieve repository chunks using BM25 keyword search."""

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

        # Build searchable text for every chunk.
        self.documents = [
            self._build_search_text(chunk)
            for chunk in chunks
        ]

        # Tokenize the repository once when the retriever is created.
        tokenized_corpus = [
            self._tokenize(document)
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """
        Tokenize text while preserving useful code identifiers.

        Examples:
            get_incident() -> get_incident
            request_id -> request_id
            /incidents -> /incidents
        """

        return re.findall(
            r"/[a-zA-Z0-9_./-]+|[a-zA-Z_][a-zA-Z0-9_]*",
            text.lower(),
        )

    @staticmethod
    def _build_search_text(chunk: dict) -> str:
        """
        Combine metadata and code into searchable text.

        This allows BM25 to search:
        - file paths
        - function/class names
        - chunk types
        - actual source code
        """

        return " ".join(
            [
                chunk.get("file_path", ""),
                chunk.get("name") or "",
                chunk.get("type") or "",
                chunk.get("content", ""),
            ]
        )

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[dict]:
        """Retrieve the most relevant chunks using BM25."""

        query_tokens = self._tokenize(query)

        
        if not query_tokens:
            return []

        scores = self.bm25.get_scores(query_tokens)

        
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indices:
            
            if scores[index] <= 0:
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "content": chunk["content"],
                    "file_path": chunk["file_path"],
                    "type": chunk["type"],
                    "name": chunk["name"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "keyword_score": float(scores[index]),
                }
            )

            
            if len(results) >= k:
                break

        return results