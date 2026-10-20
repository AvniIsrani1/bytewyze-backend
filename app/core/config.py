from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

# .env lives in the backend root, two folders above this file
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    # real environment variables win over .env (handy when deployed)
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    # min_length=1 so an empty DB_PASSWORD in .env fails loudly instead of trying to connect with no password
    db_password: str = Field(min_length=1)
    # optional path to a CA bundle, only needed if the system certificates don't recognize Azure's
    db_ssl_ca: str | None = None

    @property
    def database_url(self) -> URL:
        # URL.create escapes special characters in the password for us
        return URL.create(
            "mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": "utf8mb4"},
        )


# cached and built on first use, so the app still starts (products etc. keep working) when .env isn't filled in
@lru_cache
def get_settings() -> Settings:
    return Settings()
