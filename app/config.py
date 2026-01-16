import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "LLM API Service"
    API_KEY: str | None = os.getenv("API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "distilgpt2")
    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", 64))
    AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "secret123")

settings = Settings()
