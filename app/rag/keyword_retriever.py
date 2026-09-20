import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


class KeywordRetriever:
    """Retrieve repository chunks using a persistent BM25 index."""

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

        self.documents = [
            self._build_search_text(chunk)
            for chunk in chunks
        ]

        tokenized_corpus = [
            self._tokenize(document)
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Tokenize natural language and code identifiers for BM25 search."""
        text = text.lower()
        text = text.replace("\\", "/")
        text = text.replace("-", " ")

        tokens = re.findall(
            r"[a-z0-9_]+",
            text,
        )

        expanded_tokens = []
        for token in tokens:
            expanded_tokens.append(token)

            for part in re.split(r"[_/.]+", token):
                if part:
                    expanded_tokens.append(part)

            if "_" in token:
                expanded_tokens.extend(
                    part
                    for part in token.split("_")
                    if part
                )

        return expanded_tokens

    @staticmethod
    def _build_search_text(
        chunk: dict,
    ) -> str:
        """Build searchable text from code metadata."""

        if chunk.get("document_type") == "documentation":
            return ""

        normalized_path = str(chunk.get("file_path", "")).replace("\\", "/")
        return " ".join(
            [
                normalized_path,
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

        scores = self.bm25.get_scores(
            query_tokens
        )

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

            if (
                chunk.get("document_type")
                == "documentation"
            ):
                continue

            results.append(
                {
                    **chunk,
                    "keyword_score": float(
                        scores[index]
                    ),
                }
            )

            if len(results) >= k:
                break

        return results

    def save(
        self,
        path: str,
    ) -> None:
        """Save chunks used by the BM25 index."""

        output_path = Path(path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                self.chunks,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(
        cls,
        path: str,
    ):
        """Load chunks and rebuild the BM25 index."""

        input_path = Path(path)
        if not input_path.is_absolute():
            project_root = Path(__file__).resolve().parents[2]
            candidates = [
                project_root / input_path,
                project_root / "app" / input_path,
            ]
            for candidate in candidates:
                if candidate.exists():
                    input_path = candidate
                    break

        chunks = json.loads(
            input_path.read_text(
                encoding="utf-8"
            )
        )

        return cls(chunks)