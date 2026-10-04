from app.rag.splitter import split_documents

def test_python_funstion_is_split():
    documents = [
        {
            "content": """
def hello():
    return "hello"
""",
            "file_path": "example.py",
            "extension": ".py",
            "document_type": "code",
        }
    ]

    chunks = split_documents(documents)
    assert len(chunks) >= 1

    function_chunks = [
        chunk
        for chunk in chunks
        if chunk.get("type") == "function"

    ]

    assert len(function_chunks) == 1
    assert function_chunks[0]["name"] == "hello"