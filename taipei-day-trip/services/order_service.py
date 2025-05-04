from services.payment_service import payment_service
from repositories.payment_repository import create_payment
from repositories.order_repository import create_order, get_order_id_and_price, update_order_status
from repositories.booking_repository import delete_booking_data
from datetime import datetime
import random
import string


async def create_order_and_payment(db, user_id, payload):
    order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + \
        "".join(random.choices(string.ascii_uppercase+string.digits, k=4))

    create_order(db, user_id, payload, order_number)

    payment_result = await payment_service(payload, order_number)
    payment_status = payment_result.get("status")
    payment_rec_trade_id = payment_result.get("rec_trade_id")

    order_id_and_price = get_order_id_and_price(db, user_id, order_number)

    if payment_status == 0:
        update_order_status(db, user_id, order_number)
        create_payment(db, order_id_and_price, "success", payment_rec_trade_id)
    else:
        create_payment(db, order_id_and_price, "failed", payment_rec_trade_id)

    delete_booking_data(db, user_id)
    return order_number, payment_status
