
from pathlib import Path

from rag.embeddings import EmbeddingModel
from rag.keyword_retriever import KeywordRetriever
from rag.loader import load_repository
from rag.reranker import CodeReranker
from rag.retriever import CodeRetriever
from rag.splitter import split_documents
from rag.vectorstore import VectorStore
from rag.hybrid_retrieval import HybridRetriever

from evaluation.questions import EVALUATION_QUESTIONS



CHROMA_PATH = "./data/chroma"


def normalize_path(path: str) -> str:
    """Normalize paths for cross-platform comparison."""
    return Path(path).as_posix().lower()


def build_retrieval_pipeline():
    """Build the hybrid retrieval and reranking pipeline."""

    documents = load_repository(
                "../data/repositories/test_projects/flask-sample-app"
            )

    chunks = split_documents(documents)

    embedding_model = EmbeddingModel()

    vector_store = VectorStore(
        persist_directory=CHROMA_PATH
    )

    semantic_retriever = CodeRetriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    keyword_retriever = KeywordRetriever(chunks)

    hybrid_retriever = HybridRetriever(
        semantic_retriever=semantic_retriever,
        keyword_retriever=keyword_retriever,
    )

    reranker = CodeReranker()

    return hybrid_retriever, reranker


def evaluate():
    """Evaluate reranking performance on the test questions."""

    hybrid_retriever, reranker = (
        build_retrieval_pipeline()
    )

    total = len(EVALUATION_QUESTIONS)

    top_1_correct = 0
    top_3_correct = 0

    for item in EVALUATION_QUESTIONS:

        question = item["question"]
        expected_file = item["expected_file"]
        expected_name = item["expected_name"]

        candidates = hybrid_retriever.retrieve(
            query=question,
            k=10,
        )

        results = reranker.rerank(
            query=question,
            chunks=candidates,
            top_k=3,
        )

        print("\n================================")
        print(f"QUESTION: {question}")
        print(
            f"EXPECTED: "
            f"{expected_file} / {expected_name}"
        )
        print("================================")

        for rank, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{result['file_path']} / "
                f"{result['name']} "
                f"({result['rerank_score']:.4f})"
            )

        # -------------------------
        # Top-1 evaluation
        # -------------------------

        top_1 = results[0]

        if (
            normalize_path(top_1["file_path"])
            == normalize_path(expected_file)
            and top_1["name"] == expected_name
        ):
            top_1_correct += 1

        # -------------------------
        # Top-3 evaluation
        # -------------------------

        found_in_top_3 = any(
            normalize_path(result["file_path"])
            == normalize_path(expected_file)
            and result["name"] == expected_name
            for result in results
        )

        if found_in_top_3:
            top_3_correct += 1

    # -------------------------
    # Final results
    # -------------------------

    print("\n================================")
    print("EVALUATION RESULTS")
    print("================================")

    print(
        f"Top-1 accuracy: "
        f"{top_1_correct}/{total} "
        f"({top_1_correct / total:.2%})"
    )

    print(
        f"Top-3 accuracy: "
        f"{top_3_correct}/{total} "
        f"({top_3_correct / total:.2%})"
    )


if __name__ == "__main__":
    evaluate()

