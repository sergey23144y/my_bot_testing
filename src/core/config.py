import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_URL: str = "http://localhost:3000/api"
    REDIS_HOST: str
    REDIS_USER_NAME: str
    REDIS_USER_PASSWORD: str
    REDIS_PORT: str
    REDIS_DB: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def ger_redis_url(self) -> str:
        if self.REDIS_USER_PASSWORD:
            return f"redis://{self.REDIS_USER_NAME}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        else:
            return f"redis://{self.REDIS_USER_NAME}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
