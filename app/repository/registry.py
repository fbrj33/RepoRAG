import json
from pathlib import Path

from app.core.config import INDEXES_DIR


class RepositoryRegistry:
    def __init__(self):
        INDEXES_DIR.mkdir(parents=True, exist_ok=True)

        self.registry_path = INDEXES_DIR / "repositories.json"

        if not self.registry_path.exists():
            self.registry_path.write_text(
                json.dumps({}, indent=2),
                encoding="utf-8",
            )

    def _load(self):
        return json.loads(
            self.registry_path.read_text(encoding="utf-8")
        )

    def _save(self, data):
        self.registry_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def register(
        self,
        repository_id,
        repository_url,
        repository_path,
        index_path,
        status,
    ):
        data = self._load()

        data[repository_id] = {
            "repository_id": repository_id,
            "repository_url": repository_url,
            "repository_path": repository_path,
            "index_path": index_path,
            "status": status,
        }

        self._save(data)

    def get(self, repository_id):
        data = self._load()
        return data.get(repository_id)

    def list(self):
        data = self._load()
        return list(data.values())

    def delete(self, repository_id):
        data = self._load()

        if repository_id in data:
            del data[repository_id]
            self._save(data)

            return True

        return False