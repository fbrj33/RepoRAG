from rag.hybrid_retrieval import HybridRetriever
from rag.index_manager import RepositoryIndex
from rag.reranker import CodeReranker


class RetrievalPipeline:
    """Complete retrieval pipeline."""

    def __init__(
        self,
        repository_index: RepositoryIndex,
        reranker: CodeReranker,
    ):
        self.hybrid_retriever = HybridRetriever(
            semantic_retriever=(
                repository_index.semantic_retriever
            ),
            keyword_retriever=(
                repository_index.keyword_retriever
            ),
        )

        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        candidate_k: int = 10,
        top_k: int = 3,
    ) -> list[dict]:

        candidates = self.hybrid_retriever.retrieve(
            query=query,
            k=candidate_k,
        )

        return self.reranker.rerank(
            query=query,
            chunks=candidates,
            top_k=top_k,
        )