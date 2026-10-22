from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

frontend_origin: str = "http://localhost:5175"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")
    anthropic_api_key: SecretStr
    model_name: str
    max_tokens: int
    
settings = Settings()
