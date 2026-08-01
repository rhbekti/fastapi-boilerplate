import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Base Config Setting"""

    app_name: str = "Fast Api Boilerplate"
    db_name: str | None = os.getenv("DATABASE_URL")

    db_pool_min_size: int = 1
    db_pool_max_size: int = 10

    @property
    def db_url(self) -> str:
        """return connection string database url."""
        return f"{self.db_name}"


config = Config()
