import chromadb


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        collection_name: str = "repo_code",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings,
    ) -> None:

        documents = []
        metadatas = []
        ids = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            documents.append(chunk["content"])

            metadatas.append(
                {
                    "file_path": chunk["file_path"],
                    "extension": chunk["extension"],
                    "chunk_id": chunk["chunk_id"],
                    "type": chunk["type"],
                    "name": chunk["name"] or "",
                    "start_line": (
                        chunk["start_line"]
                        if chunk["start_line"] is not None
                        else -1
                    ),
                    "end_line": (
                        chunk["end_line"]
                        if chunk["end_line"] is not None
                        else -1
                    ),
                }
            )

            ids.append(
                f"{chunk['file_path']}::{chunk['chunk_id']}"
            )

        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query_embedding,
        k: int = 5,
    ):
        return self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=k,
        )