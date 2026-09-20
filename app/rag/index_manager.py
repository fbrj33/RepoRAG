from pathlib import Path

from rag.embeddings import EmbeddingModel
from rag.keyword_retriever import KeywordRetriever
from rag.retriever import CodeRetriever
from rag.vectorstore import VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class RepositoryIndex:
    """Load all indexes belonging to a repository."""

    def __init__(
        self,
        index_path: str,
        collection_name: str,
    ):
        self.index_path = PROJECT_ROOT / index_path

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            persist_directory=str(
                self.index_path / "chroma"
            ),
            collection_name=collection_name,
        )

        self.semantic_retriever = CodeRetriever(
            vector_store=self.vector_store,
            embedding_model=self.embedding_model,
        )

        self.keyword_retriever = KeywordRetriever.load(
            str(self.index_path / "chunks.json")
        )