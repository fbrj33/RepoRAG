from rag.embeddings import EmbeddingModel
from rag.vectorstore import VectorStore
class CodeRetriever:
    def __init__(self, vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self,query:str,
                 k:int=5) -> list[dict]:
        query_embedding = self.embedding_model.embed_query(query)

        results = self.vector_store.search(
            query_embedding,
            k=k,
        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                {
                    "content": document,
                    "file_path": metadata["file_path"],
                    "type": metadata["type"],
                    "name": metadata["name"],
                    "start_line": metadata["start_line"],
                    "end_line": metadata["end_line"],
                    "distance": distance,
                }
            )

        return retrieved_chunks