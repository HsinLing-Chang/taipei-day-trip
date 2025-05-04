from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.db import get_db
from schemas.booking import booking_form_validator
from dependencies.auth import verifytoken_wrapper
from repositories.attractions_repository import get_attraction_info
from repositories.booking_repository import fetch_bookinig_attraction, fetch_booking_record, update_booking_data, create_booking_data, delete_booking_data
router = APIRouter(prefix="/api", tags=["Booking"])


@router.post("/booking")
def booking(booking_form: booking_form_validator, db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    user_id = user_data.get("id")
    try:
        exists = fetch_booking_record(db, user_id)
        if exists:
            update_booking_data(db, booking_form, user_id)
        else:
            create_booking_data(db, booking_form, user_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/booking")
def get_booking(db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    user_id = user_data.get("id")

    try:
        booking_data = fetch_bookinig_attraction(db, user_id)
        if not booking_data:
            return {"data": None}

        attraction = get_attraction_info(
            db, booking_data.get("attractionID"))

        return {"data": {
            "attraction": attraction,
            "date": booking_data.get("booking_date"),
            "time": booking_data.get("time"),
            "price": booking_data.get("price")
        }}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/booking")
def delete_booking(db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    user_id = user_data.get("id")
    try:
        delete_booking_data(db, user_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
