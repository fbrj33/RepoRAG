from rag.loader import load_repository
from rag.splitter import split_documents
from rag.embeddings import EmbeddingModel
from rag.vectorstore import VectorStore
from rag.retriever import CodeRetriever
from rag.keyword_retriever import KeywordRetriever
from rag.hybrid_retrieval import HybridRetriever
from rag.reranker import CodeReranker
from rag.pipeline import RetrievalPipeline
from rag.generator import CodeGenerator
from rag.rag_pipeline import RagPipeline



CHROMA_PATH = "./data/chroma"


def main():


    documents = load_repository(
            "../data/repositories/test_projects/flask-sample-app"
        )
    

    print(f"Files loaded: {len(documents)}")

  

    chunks = split_documents(documents)

    print(f"Chunks generated: {len(chunks)}")

  

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

  

    retrieval_pipeline = RetrievalPipeline(
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
    )

   

    generator = CodeGenerator(
        model_name="llama3.2:3b"
    )

   

    rag_pipeline = RagPipeline(
        retrieval_pipeline=retrieval_pipeline,
        generator=generator,
    )

   

    question = (
        "Where is the item creation endpoint implemented?"
    )

    result = rag_pipeline.answer(
        question=question,
        candidate_k=10,
        top_k=3,
    )

   

    print("\n================================")
    print("REPORAG ANSWER")
    print("================================\n")

    print(result["answer"])

    

    print("\n================================")
    print("SOURCES")
    print("================================")

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):
        print(f"\n--- Source {index} ---")
        print(f"File: {source['file_path']}")
        print(f"Type: {source['type']}")
        print(f"Name: {source['name']}")
        print(
            f"Lines: "
            f"{source['start_line']}-"
            f"{source['end_line']}"
        )
        print(
            f"Rerank score: "
            f"{source['rerank_score']:.4f}"
        )


if __name__ == "__main__":
    main()