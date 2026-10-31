from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")
    anthropic_api_key: SecretStr
    model_name: str
    max_tokens: int
    app_api_key: SecretStr
    frontend_origin : list[str] = ['http://localhost:5173']
    database_url: str
    
settings = Settings()
