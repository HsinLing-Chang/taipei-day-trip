from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.db import get_db
from repositories.order_repository import get_order_data_by_order_number
from repositories.attractions_repository import get_attraction_info
from services.order_service import create_order_and_payment
from schemas.order import OrderPayload
from dependencies.auth import verifytoken_wrapper

router = APIRouter(prefix="/api", tags=["Order"])


@router.post("/orders")
async def get_response(payload: OrderPayload, db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    user_id = user_data.get("id")
    try:
        order_number, payment_status = await create_order_and_payment(
            db, user_id, payload)
        return {
            "data": {
                "number": order_number,
                "payment": {
                    "status": 0 if payment_status == 0 else 1,
                    "message": "付款成功" if payment_status == 0 else "付款失敗"
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/order/{orderNumber}")
def get_order(orderNumber: str, db=Depends(get_db), user_date=Depends(verifytoken_wrapper())):
    try:
        user_id = user_date.get("id")
        order = get_order_data_by_order_number(db, user_id, orderNumber)

        if order:
            attraction = get_attraction_info(db, order.get("attractionID"))
            order_payload = {
                "number": order.get("number"),
                "price": order.get("price"),
                "trip": {
                    "attraction": attraction,
                    "date": order.get("booking_date"),
                    "time": order.get("time")
                },
                "contact": {
                    "name": order.get("username"),
                    "email": order.get("email"),
                    "phone": order.get("phone")
                },
                "status": 0 if (order.get("status") == "paid") else 1
            }
            return {"data": order_payload}
        return {"data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
