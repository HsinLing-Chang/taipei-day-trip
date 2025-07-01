from pydantic import BaseModel, validator
from fastapi import HTTPException, status
from datetime import datetime


class booking_form_validator(BaseModel):
    attractionID: int
    date: str
    time: str
    price: int

    @validator("date")
    def validate_dates(cls, val):
        try:
            datetime.strptime(val, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="日期格式不正確")
        return val

    @validator("time")
    def validate_date(cls, val):
        if val not in ["morning", "afternoon"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="時間欄位必須為'morning'或'afternoon'")
        return val

    @validator("price")
    def validate_price(cls, val):
        if val not in [2000, 2500]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="價格不正確")
        return val
