from rag.index_manager import RepositoryIndex
from rag.pipeline import RetrievalPipeline
from rag.reranker import CodeReranker
from rag.context import build_context
from rag.generator import CodeGenerator


INDEX_PATH = "data/indexes/real_project"
COLLECTION_NAME = "real_project"


def main():
    print("Loading repository index...")

    repository_index = RepositoryIndex(
        index_path=INDEX_PATH,
        collection_name=COLLECTION_NAME,
    )

    reranker = CodeReranker()

    pipeline = RetrievalPipeline(
        repository_index=repository_index,
        reranker=reranker,
    )

    question = input(
        "\nAsk a question about the repository: "
    )

    results = pipeline.retrieve(
        query=question,
        candidate_k=10,
        top_k=5,
    )

    print("\n================================")
    print("RETRIEVAL RESULTS")
    print("================================")

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\n{rank}. "
            f"{result['file_path']} "
            f"/ {result['name']}"
        )

        print(
            f"Type: {result['type']}"
        )

        print(
            f"Lines: "
            f"{result['start_line']}-"
            f"{result['end_line']}"
        )

        print(
            f"RRF score: "
            f"{result.get('rrf_score', 0):.4f}"
        )

        print(
            f"Reranker score: "
            f"{result['rerank_score']:.4f}"
        )

        print("\nCode:")
        print(result["content"])

    context = build_context(results)
    generator = CodeGenerator()
    answer = generator.generate(
        question=question,
        context=context,
    )

    print("\n================================")
    print("ANSWER")
    print("================================")
    print(answer)


if __name__ == "__main__":
    main()