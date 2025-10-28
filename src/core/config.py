import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
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

    def create_bot(self) -> Bot:
        return Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    def ger_redis_url(self) -> str:
        if self.REDIS_USER_PASSWORD:
            return f"redis://{self.REDIS_USER_NAME}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        else:
            return f"redis://{self.REDIS_USER_NAME}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
bot = settings.create_bot()
