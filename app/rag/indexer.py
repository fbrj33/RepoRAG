from pathlib import Path

from rag.embeddings import EmbeddingModel
from rag.keyword_retriever import KeywordRetriever
from rag.loader import load_repository
from rag.splitter import split_documents
from rag.vectorstore import VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class RepositoryIndexer:
    """Build all searchable indexes for a repository."""

    def __init__(
        self,
        repository_path: str,
        index_path: str,
        collection_name: str,
    ):
        self.repository_path = PROJECT_ROOT / repository_path
        self.index_path = PROJECT_ROOT / index_path

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            persist_directory=str(
                self.index_path / "chroma"
            ),
            collection_name=collection_name,
        )

    def index(self) -> dict:
        """Load, split, embed and persist repository indexes."""

        documents = load_repository(
            str(self.repository_path)
        )

        print(
            f"Files loaded: {len(documents)}"
        )

        chunks = split_documents(documents)

        print(
            f"Chunks generated: {len(chunks)}"
        )

        if not chunks:
            raise ValueError(
                "No supported files were found "
                "in the repository."
            )

        print("Building BM25 index...")

        keyword_retriever = KeywordRetriever(
            chunks
        )

        keyword_index_path = (
            self.index_path / "chunks.json"
        )

        keyword_retriever.save(
            str(keyword_index_path)
        )

        print(
            f"BM25 index saved to: "
            f"{keyword_index_path}"
        )

        print("Generating embeddings...")

        embeddings = (
            self.embedding_model.embed_documents(
                [
                    chunk["content"]
                    for chunk in chunks
                ]
            )
        )

        print("Storing chunks in Chroma...")

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        print("Indexing completed.")

        return {
            "files": len(documents),
            "chunks": len(chunks),
            "index_path": str(self.index_path),
        }


if __name__ == "__main__":

    REPOSITORY_PATH = (
        "data/repositories/real_project"
    )

    INDEX_PATH = (
        "data/indexes/real_project"
    )

    indexer = RepositoryIndexer(
        repository_path=REPOSITORY_PATH,
        index_path=INDEX_PATH,
        collection_name="real_project",
    )

    result = indexer.index()

    print("\n================================")
    print("INDEXING SUMMARY")
    print("================================")

    print(
        f"Files: {result['files']}"
    )

    print(
        f"Chunks: {result['chunks']}"
    )

    print(
        f"Index: {result['index_path']}"
    )