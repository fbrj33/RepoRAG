from rag.index_manager import RepositoryIndex
from rag.hybrid_retrieval import HybridRetriever
from rag.reranker import CodeReranker


def main():
    index = RepositoryIndex(
        index_path="data/indexes/real_project",
        collection_name="real_project",
    )

    query = "Where is the scheduled report implemented?"

    hybrid = HybridRetriever(
        semantic_retriever=index.semantic_retriever,
        keyword_retriever=index.keyword_retriever,
    )

    print("\n========== HYBRID ==========")

    hybrid_results = hybrid.retrieve(
        query,
        k=10,
        semantic_k=10,
        keyword_k=10,
    )

    print(f"Results: {len(hybrid_results)}")

    for result in hybrid_results:
        print(
            result["file_path"],
            "/",
            result.get("name"),
            "| RRF:",
            result.get("rrf_score"),
        )

    print("\n========== RERANKER ==========")

    reranker = CodeReranker()

    reranked = reranker.rerank(
        query,
        hybrid_results,
        top_k=10,
    )

    print(f"Results: {len(reranked)}")

    for result in reranked:
        print(
            result["file_path"],
            "/",
            result.get("name"),
            "| Rerank:",
            result.get("rerank_score"),
        )


if __name__ == "__main__":
    main()