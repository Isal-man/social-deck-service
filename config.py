from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    X_APP_KEY: str
    X_APP_SECRET_KEY: str
    X_CLIENT_ID: str
    X_CLIENT_SECRET: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()