from pydantic import BaseModel, validator
from fastapi import HTTPException, status
import re


class AttactionInfo(BaseModel):
    id: int
    name: str
    address: str
    image: str


class TripInfo(BaseModel):
    attraction: AttactionInfo
    date: str
    time: str


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

    @validator("name")
    def name_validator(cls, val):
        if not val:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="姓名不可為空值")
        return val

    @validator("email")
    def email_validator(cls, val):
        if "@" not in val:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email格式不正確")
        return val

    @validator("phone")
    def phone_validator(cls, val):
        regex = r"^09\d{8}$"
        if re.match(regex, val):
            return val
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="手機號碼格式不正確")


class OrderInfo(BaseModel):
    price: int
    trip: TripInfo
    contact: ContactInfo


class OrderPayload(BaseModel):
    prime: str
    order: OrderInfo
