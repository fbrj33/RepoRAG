from rag.hybrid_retrieval import HybridRetriever
from rag.reranker import CodeReranker

class RetrievalPipeline:
    def __init__(
            self,
            hybrid_retriever: HybridRetriever,
            reranker: CodeReranker,
    ):
        self.hybrid_retriever = hybrid_retriever
        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        candidate_k: int = 10,
        top_k: int = 3,
    ) -> list[dict]:

        hybrid_results = self.hybrid_retriever.retrieve(
            query=query,
            k=candidate_k,
        )
        reranked_results = self.reranker.rerank(
            query=query,
            chunks=hybrid_results,
            top_k=top_k,
        )
        return reranked_results