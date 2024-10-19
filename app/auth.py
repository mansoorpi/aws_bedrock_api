# app/auth.py
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from .config import settings   # Adjust import to match config.py location
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch username and password from .env
SERVICE_ACCOUNT_USERNAME = os.getenv("SERVICE_ACCOUNT_USERNAME")
SERVICE_ACCOUNT_PASSWORD = os.getenv("SERVICE_ACCOUNT_PASSWORD")

# Authenticate the user using credentials from .env
def authenticate_user(username: str, password: str) -> bool:
    return username == SERVICE_ACCOUNT_USERNAME and password == SERVICE_ACCOUNT_PASSWORD

# Create the JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

# Verify the token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != SERVICE_ACCOUNT_USERNAME:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
