import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key-change-in-prod')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def tokengen(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def tokenver(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise JWTError("Invalid token payload")

        return username

    except JWTError:
        raise JWTError("Token is invalid or expired")