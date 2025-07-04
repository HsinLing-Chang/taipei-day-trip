# 處理api/user/auth
from dependencies.db import get_db
from fastapi import Depends,  APIRouter, HTTPException, status
from schemas.user import sing_in_form, sign_up_form
from utils.jwt import jwt_encode
from dependencies.auth import verifytoken_wrapper
from utils.hash import Hash
from repositories.user_repository import get_user_email, create_user, get_user_data_by_email
router = APIRouter(prefix="/api", tags=["User"])


@router.post("/user")
def sign_up(formData: sign_up_form, db=Depends(get_db)):
    email = get_user_email(db, formData.email)
    if email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="帳號已被註冊，請重新嘗試")
    try:
        hashed_password = Hash.bcrypt(formData.password)
        create_user(db, formData.name, formData.email,  hashed_password)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="註冊時發生錯誤，請稍後再試")


@router.put("/user/auth")
def sign_in(formDate: sing_in_form, db=Depends(get_db)):
    user_data = get_user_data_by_email(db, formDate.email)

    if not user_data or not Hash.verify_password(formDate.password, user_data.get("password")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="帳號或密碼錯誤，請重新嘗試。")
    token = jwt_encode(user_data)
    return {"token": token}


@router.get("/user/auth")
def get_user(user_data=Depends(verifytoken_wrapper(return_none=True))):
    if user_data:
        return {"data": user_data}
    return {"data": None}
