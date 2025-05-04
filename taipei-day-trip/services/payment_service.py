import httpx
import os
from dotenv import load_dotenv

load_dotenv()
PARNER_KEY = os.getenv("PARNER_KEY")


async def payment_service(payload, order_number):
    prime = payload.prime
    order = payload.order
    trip = order.trip
    attraction = trip.attraction
    contact = order.contact
    tappay_payload = {
        "prime": prime,
        "partner_key": PARNER_KEY,
        "merchant_id": "DummyCompany_FUBON_POS_1",
        "details": attraction.name,
        "amount": order.price,
        "order_number": order_number,
        "cardholder": {
            "phone_number": contact.phone,
            "name": contact.name,
            "email": contact.email,
        },
        "remember": False,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": PARNER_KEY,
    }
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=tappay_payload, headers=headers)
        payment_result = response.json()

    return payment_result
