from pathlib import Path

from app.rag.keyword_retriever import KeywordRetriever
from app.rag.retriever import CodeRetriever
from app.rag.vectorstore import VectorStore


class RepositoryIndex:
    def __init__(
        self,
        index_path,
        collection_name,
        embedding_model,
    ):
        self.index_path = Path(index_path)

        self.vector_store = VectorStore(
            persist_directory=str(self.index_path / "chroma"),
            collection_name=collection_name,
        )

        self.semantic_retriever = CodeRetriever(
            vector_store=self.vector_store,
            embedding_model=embedding_model,
        )

        self.keyword_retriever = KeywordRetriever.load(
            str(self.index_path / "chunks.json")
        )