from rag.loader import load_repository

documents = load_repository(
    "data/repositories/test_projects/flask-sample-app/app"
)

print(f"loaded {len(documents)} files")

for document in documents [:5]:
    print(
        document["file_path"],
        document["extension"],
    )
      