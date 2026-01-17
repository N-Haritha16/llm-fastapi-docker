from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "LLM API"
    API_KEY: str
    MODEL_NAME: str = "sshleifer/tiny-gpt2"
    MAX_NEW_TOKENS: int = 64

    class Config:
        env_file = ".env"

settings = Settings()
