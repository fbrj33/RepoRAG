from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPOSITORIES_DIR = PROJECT_ROOT / "data" / "repositories"
INDEXES_DIR = PROJECT_ROOT / "data" / "indexes"


# AI models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
LLM_MODEL = "llama3.2:3b"


# Retrieval settings
DEFAULT_CANDIDATE_K = 10
DEFAULT_TOP_K = 5