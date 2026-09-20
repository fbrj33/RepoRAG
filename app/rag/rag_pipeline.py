from rag.context import build_context
from rag.generator import CodeGenerator
from rag.pipeline import RetrievalPipeline


class RagPipeline:
    def __init__(
            self,
            retrieval_pipeline: RetrievalPipeline,
            generator: CodeGenerator,

    ):
        self.retrieval_pipeline = retrieval_pipeline
        self.generator = generator

    def answer(
            self,
            question:str,
            candidate_k: int=10,
            top_k : int=3,

    ) -> dict:

        retrieved_chunks = self.retrieval_pipeline.retrieve(
            query=question,
            candidate_k=candidate_k,
            top_k=top_k,
        )

        context = build_context(retrieved_chunks)

        answer = self.generator.generate(
            question=question,
            context=context,
    
        )

        return {
            "answer": answer,
            "sources": retrieved_chunks,
            "context":context,

        }