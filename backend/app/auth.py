from typing import Annotated
from fastapi import Header, HTTPException
from app.settings import settings

def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key is None or x_api_key != settings.app_api_key.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
