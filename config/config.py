import yaml
import os


class Config:
    def __init__(self, file="config.yaml", logger=None):
        self._logger = logger
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, file)
        self._data = self.load_yaml(path)

    def load_yaml(self, path) -> dict:
        if not os.path.exists(path):
            if self._logger:
                self._logger.error(f"YAML config not found: {path}")
            os._exit(1)

        with open(path, "r") as f:
            return yaml.safe_load(f)

    def get(self, key: str) -> str | list[str]:
        if key in ("text", "image"):
            return self._data.get("post").get(key)
        return self._data.get(key)
