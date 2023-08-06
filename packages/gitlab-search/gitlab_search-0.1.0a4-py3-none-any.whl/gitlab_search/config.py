"""Handle the app's configuration."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

CONFIG_FILENAME = ".gitlabsearch"
DEFAULT_URL = "https://gitlab.com"


@dataclass
class Config:
    """A configuration for this app."""

    token: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        if not self.url:
            self.url = DEFAULT_URL

    def is_valid(self) -> bool:
        return bool(self.token) and bool(self.url)

    def save(self) -> Path:
        if not self.token or not self.url:
            raise ValueError("Can not store incomplete config.")

        data = {"token": self.token, "url": self.url}
        path = self.path()
        with path.open("w") as fp:
            json.dump(data, fp)
        return path.absolute()

    @classmethod
    def load(cls) -> "Config":
        try:
            with cls.path().open("r") as fp:
                data = json.load(fp)
            return cls(token=str(data["token"]), url=str(data["url"]))
        except OSError:
            return cls()

    @staticmethod
    def path() -> Path:
        return Path.home() / CONFIG_FILENAME
