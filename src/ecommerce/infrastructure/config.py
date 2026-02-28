import sys

from pydantic import ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = {"env_file": ".env", "extra": "ignore"}


try:
    settings = Settings()
except ValidationError as e:
    missing_vars = [err["loc"][0] for err in e.errors() if err["type"] == "missing"]
    if missing_vars:
        print(
            f"ERROR: Missing required environment variables: {', '.join(str(v).upper() for v in missing_vars)}",
            file=sys.stderr,
        )
        print(
            "Please set them in .env file or as environment variables.",
            file=sys.stderr,
        )
    sys.exit(1)
