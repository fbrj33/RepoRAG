import hashlib
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

from git import Repo
from app.core.config import REPOSITORIES_DIR

class RepositoryManager:
    def __init__(
            self,
            repositories_dir:Path = REPOSITORIES_DIR,

    ):
        self.repositories_dir= repositories_dir
        self.repositories_dir.mkdir(
            parents=True,
            exist_ok=True,

        )
    @staticmethod
    def normalize_url(repo_url:str) -> str:
        repo_url = repo_url.strip()

        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]

        return repo_url.rstrip("/")

    @classmethod
    def repository_id(cls, repo_url: str) -> str:
        normalized_url = cls.normalize_url(repo_url)

        parsed = urlparse(normalized_url)

        path = parsed.path.strip("/")

        name = path.split("/")[-1]

        name = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            name,
        )

        digest = hashlib.sha256(
            normalized_url.encode("utf-8")
        ).hexdigest()[:8]

        return f"{name}_{digest}"
    def repository_path(
        self,
        repo_url: str,
    ) -> Path:
        repository_id = self.repository_id(
            repo_url
        )

        return (
            self.repositories_dir
            / repository_id
        )

    def exists(
        self,
        repo_url: str,
    ) -> bool:
        return self.repository_path(
            repo_url
        ).exists()

    def clone(
        self,
        repo_url: str,
    ) -> dict:

        repo_url = self.normalize_url(
            repo_url
        )

        repository_id = self.repository_id(
            repo_url
        )
        destination = (
            self.repositories_dir
            / repository_id
        )

        if destination.exists():
            return {
                "repository_id": repository_id,
                "repository_path": str(
                    destination
                ),
                "status": "already_exists",
                "url": repo_url,
            }

        try:
            Repo.clone_from(
                repo_url,
                destination,
                depth=1,
            )

        except Exception:
            if destination.exists():
                shutil.rmtree(
                    destination,
                    ignore_errors=True,
                )

            raise
        return {
            "repository_id": repository_id,
            "repository_path": str(
                destination
            ),
            "status": "cloned",
            "url": repo_url,
        }


    

