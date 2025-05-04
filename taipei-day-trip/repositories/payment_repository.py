def create_payment(db, user_order, status, rec_trade_id):
    db.execute("INSERT INTO payment (order_id, price, status, rec_trade_id) VALUES (%s,%s,%s,%s)",
               (user_order.get("id"), user_order.get("price"), status, rec_trade_id))
