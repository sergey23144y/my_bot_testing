from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    api_key: str
    api_url: str = "https://jsonplaceholder.typicode.com/posts/1"
    redis_host: str
    redis_user_name: str
    redis_user_password: str
    redis_port: str
    redis_db: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def ger_redis_url(self) -> str:
        if self.redis_user_password:
            return f"redis://{self.redis_user_name}:{self.redis_user_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        else:
            return f"redis://{self.redis_user_name}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()
