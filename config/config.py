from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    twitter_client_id: str
    twitter_client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()