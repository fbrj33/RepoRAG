from pathlib import Path
from app.rag.loader import load_repository

def test_loader_finds_python_files(tmp_path):
    test_file = Path(tmp_path) / "example.py"

    test_file.write_text(
        "def hello():\n    return 'hello'\n",
        encoding="utf-8",
    )

    documents = load_repository(str(tmp_path))

    assert len(documents) == 1
    assert documents[0]["extension"] == ".py"
    assert "def hello" in documents[0]["content"]