import json
from pathlib import Path
from app.core.config import INDEXES_DIR

class RepositoryRegistry:

    def __init__(
        self,
        index_dir: Path = INDEXES_DIR,

        ):
        self.index_dir = index_dir 
        self.index_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.registry_path = (
            self.index_dir
            / "repositories.json"
            )

    def _load(self) -> dict:
        if not self.registry_path.exists():
            return {}

        return json.loads(
            self.registry_path.read_text(
                encoding="utf-8"
            )
        )

    def _save(
        self,
        data: dict,
    ) -> None:
        self.registry_path.write_text(
            json.dumps(
                data,
                indent=2,
            ),
            encoding="utf-8",
        )

    def register(
        self,
        repository_id: str,
        repo_url: str,
        repository_path: str,
        index_path: str,
    ) -> None:

        data = self._load()
        data[repository_id] = {
            "repository_id": repository_id,
            "repo_url": repo_url,
            "repository_path": repository_path,
            "index_path": index_path,
        }

        self._save(data)

    def get(
        self,
        repository_id: str,
    ) -> dict | None:

        return self._load().get(
            repository_id
        )

    def list(self) -> list[dict]:
        return list(
            self._load().values()
        )

       

       
