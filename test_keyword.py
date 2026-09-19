from rag.loader import load_repository
from rag.splitter import split_documents
from rag.keyword_retriever import KeywordRetriever


REPOSITORY_PATH = "data/repositories/test_project"


def main():
    print("Loading repository...")

    documents = load_repository(
    "../data/repositories/test_projects/flask-sample-app"
    )

    print(
        f"Files loaded: {len(documents)}"
    )

    chunks = split_documents(documents)

    print(
        f"Chunks generated: {len(chunks)}"
    )

    retriever = KeywordRetriever(chunks)

    query = "get_items"

    results = retriever.retrieve(
        query,
        k=5,
    )

    print("\n===== KEYWORD SEARCH RESULTS =====")

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
            f"BM25 score: "
            f"{result['keyword_score']:.4f}"
        )

        print("\nCode:")
        print(result["content"])


if __name__ == "__main__":
    main()