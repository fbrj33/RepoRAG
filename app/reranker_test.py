from rag.loader import load_repository
from rag.splitter import split_documents
from rag.reranker import CodeReranker

def main():
    documents = load_repository(
        "../data/repositories/test_projects/flask-sample-app"
    )
    chunks = split_documents(documents)
    reranker = CodeReranker()

    query = "where is the item creation endpoint implemented?"

    results = reranker.rerank(query=query,
                              chunks=chunks,
                              top_k=5,
                              )
    print(f"Reranked results for query: '{query}'")
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
            f"Rerank score: "
            f"{result['rerank_score']:.4f}"
        )

         print("\nCode:")
         print(result["content"])

if __name__ == "__main__":
     main()

        