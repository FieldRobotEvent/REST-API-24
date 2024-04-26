from .database import Database
from .databases.databases import SUPPORTED_DATABASES


class DatabaseFactory():
    _config = {}

    def get_database(self, Name: str) -> Database:
        cfg = self._config[Name]
        constructor = SUPPORTED_DATABASES[Name]
        return constructor(**cfg)

    @classmethod
    def initialise_databases(cls, **kwargs):
        for name in SUPPORTED_DATABASES.keys():
            prefix = f"{name.lower()}_"
            args = {k.removeprefix(prefix): v for (k, v) in kwargs.items()
                    if k.startswith(prefix)}
            cls._config[name] = args
