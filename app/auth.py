from fastapi import Header, HTTPException, status
from app.config import settings


def verify_token(x_api_key: str = Header(...)) -> None:
    expected = settings.API_KEY

    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
