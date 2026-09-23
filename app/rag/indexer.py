from pathlib import Path

from app.core.config import (
    EMBEDDING_MODEL,
)
from app.rag.embeddings import EmbeddingModel
from app.rag.keyword_retriever import KeywordRetriever
from app.rag.loader import load_repository
from app.rag.splitter import split_documents
from app.rag.vectorstore import VectorStore


class RepositoryIndexer:
    """Build all searchable indexes for a repository."""

    def __init__(
        self,
        repository_path: str,
        index_path: str,
        collection_name: str,
    ):
        self.repository_path = Path(
            repository_path
        )

        self.index_path = Path(
            index_path
        )

        self.index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.collection_name = (
            collection_name
        )

        self.embedding_model = (
            EmbeddingModel(
                model_name=EMBEDDING_MODEL
            )
        )

        self.vector_store = VectorStore(
            persist_directory=str(
                self.index_path / "chroma"
            ),
            collection_name=collection_name,
        )

    def index(self) -> dict:

        documents = load_repository(
            str(self.repository_path)
        )

        print(
            f"Files loaded: {len(documents)}"
        )

        chunks = split_documents(
            documents
        )

        print(
            f"Chunks generated: {len(chunks)}"
        )

        if not chunks:
            raise ValueError(
                "No supported files found."
            )

        keyword_retriever = (
            KeywordRetriever(chunks)
        )

        keyword_index_path = (
            self.index_path
            / "chunks.json"
        )

        keyword_retriever.save(
            str(keyword_index_path)
        )

        print(
            "Generating embeddings..."
        )

        embeddings = (
            self.embedding_model
            .embed_documents(
                [
                    chunk["content"]
                    for chunk in chunks
                ]
            )
        )

        print(
            "Storing vectors..."
        )

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return {
            "files": len(documents),
            "chunks": len(chunks),
            "index_path": str(
                self.index_path
            ),
            "collection_name": (
                self.collection_name
            ),
        }