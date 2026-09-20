from rag.loader import load_repository
from rag.splitter import split_documents
from rag.embeddings import EmbeddingModel
from rag.vectorstore import VectorStore
from rag.retriever import CodeRetriever
from rag.keyword_retriever import KeywordRetriever
from rag.hybrid_retrieval import HybridRetriever
from rag.reranker import CodeReranker
from rag.pipeline import RetrievalPipeline

CHROMA_PATH = "./data/chroma"

def main():
    # Load repository
    documents = load_repository(
        "../data/repositories/test_projects/flask-sample-app"
    )

    print(f"Files loaded: {len(documents)}")

    # Split repository into chunks
    chunks = split_documents(documents)

    print(f"Chunks generated: {len(chunks)}")

    # Embeddings + vector store
    embedding_model = EmbeddingModel()

    vector_store = VectorStore(
        persist_directory=CHROMA_PATH
    )

    # Semantic retriever
    semantic_retriever = CodeRetriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    # Keyword retriever
    keyword_retriever = KeywordRetriever(chunks)

    # Hybrid retriever
    hybrid_retriever = HybridRetriever(
        semantic_retriever=semantic_retriever,
        keyword_retriever=keyword_retriever,
    )

    # Reranker
    reranker = CodeReranker()

    # Complete retrieval pipeline
    pipeline = RetrievalPipeline(
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
    )

    query = "add_items"

    results = pipeline.retrieve(
        query=query,
        candidate_k=10,
        top_k=3,
    )

    print("\n===== HYBRID + RERANKER RESULTS =====")

    for index, result in enumerate(
        results,
        start=1,
    ):
        print(f"\n--- Result {index} ---")

        print(f"File: {result['file_path']}")
        print(f"Type: {result['type']}")
        print(f"Name: {result['name']}")

        print(
            f"Lines: "
            f"{result['start_line']}-"
            f"{result['end_line']}"
        )

        print(
            f"RRF score: "
            f"{result.get('rrf_score', 'N/A')}"
        )

        print(
            f"Rerank score: "
            f"{result['rerank_score']:.4f}"
        )

        print(
            f"Semantic rank: "
            f"{result.get('semantic_rank', 'N/A')}"
        )

        print(
            f"Keyword rank: "
            f"{result.get('keyword_rank', 'N/A')}"
        )

        print("\nCode:")
        print(result["content"])


if __name__ == "__main__":
    main()