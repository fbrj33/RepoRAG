from rag.loader import load_repository
from rag.splitter import split_documents
from rag.embeddings import EmbeddingModel
from rag.vectorstore import VectorStore
from rag.retriever import CodeRetriever
from rag.keyword_retriever import KeywordRetriever
from rag.hybrid_retrieval import HybridRetriever


REPOSITORY_PATH = "data/repositories/test_project"
CHROMA_PATH = "./data/chroma"


def main():
    # -------------------------
    # Load repository
    # -------------------------

    documents = load_repository(
    "../data/repositories/test_projects/flask-sample-app"
)

    print(
        f"Files loaded: {len(documents)}"
    )

    # -------------------------
    # Split repository
    # -------------------------

    chunks = split_documents(documents)

    print(
        f"Chunks generated: {len(chunks)}"
    )

    # -------------------------
    # Create semantic retriever
    # -------------------------

    embedding_model = EmbeddingModel()

    vector_store = VectorStore(
        persist_directory=CHROMA_PATH
    )

    semantic_retriever = CodeRetriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    # -------------------------
    # Create keyword retriever
    # -------------------------

    keyword_retriever = KeywordRetriever(
        chunks
    )

    # -------------------------
    # Create hybrid retriever
    # -------------------------

    hybrid_retriever = HybridRetriever(
        semantic_retriever=semantic_retriever,
        keyword_retriever=keyword_retriever,
    )

    # -------------------------
    # Query
    # -------------------------

    query = "get_items"

    results = hybrid_retriever.retrieve(
        query,
        k=5,
    )

    # -------------------------
    # Display results
    # -------------------------

    print(
        "\n===== HYBRID SEARCH RESULTS ====="
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\n--- Result {index} ---"
        )

        print(
            f"File: {result['file_path']}"
        )

        print(
            f"Type: {result['type']}"
        )

        print(
            f"Name: {result['name']}"
        )

        print(
            f"Lines: "
            f"{result['start_line']}-"
            f"{result['end_line']}"
        )

        print(
            f"RRF score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"Semantic rank: "
            f"{result['semantic_rank']}"
        )

        print(
            f"Keyword rank: "
            f"{result['keyword_rank']}"
        )

        print("\nCode:")
        print(result["content"])


if __name__ == "__main__":
    main()