from rag.loader import load_repository
from rag.splitter import split_documents


documents = load_repository(
    "data/repositories/test_projects/flask-sample-app/app"
)

chunks = split_documents(documents)

print(f"Files loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

print("\n--- Example chunks ---")

for chunk in chunks:
    print("\nFile:", chunk["file_path"])
    print("Type:", chunk["type"])
    print("Name:", chunk["name"])
    print(
        "Lines:",
        chunk["start_line"],
        "-",
        chunk["end_line"],
    )
    print("Chunk:", chunk["chunk_id"])
    print("Content:")
    print(chunk["content"])
    print("-" * 60)