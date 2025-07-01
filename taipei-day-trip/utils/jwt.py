# 純encode & decode JWT
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
import jwt
from dotenv import load_dotenv
import os
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")


def jwt_encode(user_data: dict):
    expire_time = datetime.now(tz=timezone.utc) + timedelta(days=7)
    payload = {
        "id": user_data.get("id"),
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "exp": expire_time
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token


def jwt_decode(token: str, return_none: bool):
    try:
        payload = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return payload

    except jwt.ExpiredSignatureError as e:
        if return_none:
            return None
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
    except jwt.exceptions.PyJWTError as e:
        if return_none:
            return None
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
