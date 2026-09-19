import ast

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_python_file(
    content: str,
    file_path: str,
) -> list[dict]:
    """Split Python code into logical functions/classes."""

    chunks = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Fall back to normal text splitting if parsing fails
        return split_generic_file(content, file_path)

    lines = content.splitlines()

    for node in ast.walk(tree):
        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        ):
            continue

        start_line = node.lineno
        end_line = node.end_lineno

        code = "\n".join(
            lines[start_line - 1 : end_line]
        )

        chunks.append(
            {
                "content": code,
                "file_path": file_path,
                "extension": ".py",
                "chunk_id": len(chunks),
                "type": (
                    "class"
                    if isinstance(node, ast.ClassDef)
                    else "function"
                ),
                "name": node.name,
                "start_line": start_line,
                "end_line": end_line,
            }
        )

    return chunks


def split_generic_file(
    content: str,
    file_path: str,
    extension: str = "",
) -> list[dict]:
    """Split non-Python files using recursive text splitting."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    text_chunks = splitter.split_text(content)

    return [
        {
            "content": chunk,
            "file_path": file_path,
            "extension": extension,
            "chunk_id": index,
            "type": "text",
            "name": None,
            "start_line": None,
            "end_line": None,
        }
        for index, chunk in enumerate(text_chunks)
    ]


def split_documents(documents: list[dict]) -> list[dict]:
    """Split repository documents using code-aware strategies."""

    chunks = []

    for document in documents:
        if document["extension"] == ".py":
            file_chunks = split_python_file(
                document["content"],
                document["file_path"],
            )
        else:
            file_chunks = split_generic_file(
                document["content"],
                document["file_path"],
                document["extension"],
            )

        chunks.extend(file_chunks)

    return chunks