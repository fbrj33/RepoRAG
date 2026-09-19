from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
}


def load_repository(repo_path: str) -> list[dict]:
    
    repository = Path(repo_path)

    documents = []

    for file_path in repository.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        documents.append(
            {
                "content": content,
                "file_path": str(file_path.relative_to(repository)),
                "extension": file_path.suffix.lower(),
            }
        )

    return documents