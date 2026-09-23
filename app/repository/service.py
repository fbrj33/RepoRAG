from pathlib import Path

from app.core.config import INDEXES_DIR
from app.rag.index_manager import RepositoryIndex
from app.rag.indexer import RepositoryIndexer
from app.repository.manager import (
    RepositoryManager,
)
from app.repository.registry import (
    RepositoryRegistry,
)


class RepositoryService:
    """Manage cloning and indexing repositories."""

    def __init__(self):
        self.manager = RepositoryManager()
        self.registry = RepositoryRegistry()

    def index_repository(
        self,
        repo_url: str,
    ) -> dict:

        clone_result = self.manager.clone(
            repo_url
        )

        repository_id = (
            clone_result["repository_id"]
        )

        repository_path = Path(
            clone_result["repository_path"]
        )

        index_path = (
            INDEXES_DIR
            / repository_id
        )

        collection_name = (
            f"repo_{repository_id}"
        )

        indexer = RepositoryIndexer(
            repository_path=str(
                repository_path
            ),
            index_path=str(
                index_path
            ),
            collection_name=collection_name,
        )

        result = indexer.index()

        self.registry.register(
            repository_id=repository_id,
            repo_url=repo_url,
            repository_path=str(
                repository_path
            ),
            index_path=str(
                index_path
            ),
        )

        return {
            "repository_id": repository_id,
            "repository_url": repo_url,
            "repository_path": str(
                repository_path
            ),
            "index_path": str(
                index_path
            ),
            "status": "indexed",
            "files": result["files"],
            "chunks": result["chunks"],
        }

    def get_index(
        self,
        repository_id: str,
    ) -> RepositoryIndex:

        metadata = self.registry.get(
            repository_id
        )

        if metadata is None:
            raise ValueError(
                "Repository has not been indexed."
            )

        index_path = metadata[
            "index_path"
        ]

        return RepositoryIndex(
            index_path=index_path,
            collection_name=(
                f"repo_{repository_id}"
            ),
        )