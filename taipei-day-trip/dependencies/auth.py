# get current user & verify
from typing import Optional
from fastapi import Header, HTTPException, status
from utils.jwt import jwt_decode


def verifytoken_wrapper(return_none: bool = False):
    def verify_token(authorization: Optional[str] = Header(None)):
        if not authorization or not authorization.startswith("Bearer"):
            if return_none:
                return None
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invaild or missing token")
        token = authorization.split(" ")[1]
        userData = jwt_decode(token, return_none)
        return userData
    return verify_token
