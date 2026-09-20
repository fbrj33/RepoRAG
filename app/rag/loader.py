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
    """Load supported repository files."""

    repository = Path(repo_path)
    documents = []

    for file_path in repository.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Ignore repository metadata and generated files
        if any(
            part in {
                ".git",
                ".venv",
                "venv",
                "__pycache__",
                "node_modules",
            }
            for part in file_path.parts
        ):
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        relative_path = str(
            file_path.relative_to(repository)
        ).replace("\\", "/")

        document_type = (
            "documentation"
            if file_path.name.lower()
            in {
                "readme.md",
                "readme.txt",
            }
            else "code"
        )

        documents.append(
            {
                "content": content,
                "file_path": relative_path,
                "extension": file_path.suffix.lower(),
                "document_type": document_type,
            }
        )

    return documents