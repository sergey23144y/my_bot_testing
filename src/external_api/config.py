from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    api_key: str
    api_url: str = "https://jsonplaceholder.typicode.com/posts/1"

    class Config:
        env_file = ".env"


settings = Settings()
