from pathlib import Path
from rag.loader import load_repository
from rag.retriever import CodeRetriever
from rag.embeddings import EmbeddingModel
from rag.vectorstore import VectorStore
from rag.splitter import split_documents
from rag.context import build_context
from rag.generator import CodeGenerator



PROJECT_ROOT = Path(__file__).resolve().parent.parent

 


CHROMA_PATH = (
    PROJECT_ROOT
    / "data"
    / "chroma"
)


# 1. Load repository
documents = load_repository(
    "../data/repositories/test_projects/flask-sample-app"
)

print(f"Files loaded: {len(documents)}")


# 2. Split files
chunks = split_documents(documents)

print(f"Chunks created: {len(chunks)}")


# 3. Create embeddings
embedding_model = EmbeddingModel()

texts = [
    chunk["content"]
    for chunk in chunks
]

embeddings = embedding_model.embed_documents(
    texts
)

print(
    f"Generated {len(embeddings)} embeddings"
)


# 4. Store embeddings
vector_store = VectorStore(
    persist_directory=str(CHROMA_PATH)
)

vector_store.add_chunks(
    chunks,
    embeddings,
)

print("Chunks stored in ChromaDB")


# 5. Create retriever
retriever = CodeRetriever(
    vector_store=vector_store,
    embedding_model=embedding_model,
)


# 6. Ask a question
question = "Where are items created?"

results = retriever.retrieve(
    question,
    k=5,
)
context = build_context(results)
generator = CodeGenerator()

answer = generator.generate(
    question=question,
    context=context,
)

print("\n===== GENERATED ANSWER =====")
print(answer)




