def create_order(db, user_id, payload, order_number):
    order = payload.order
    trip = order.trip
    attraction = trip.attraction
    contact = order.contact
    query_stat = "INSERT INTO orders (user_id, username, email, phone, number, status, price, booking_date, time, attractionID)" \
        "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = (user_id, contact.name, contact.email, contact.phone, order_number,
              "unpaid", order.price, trip.date, trip.time, attraction.id)
    db.execute(query_stat, params)


def get_order_id_and_price(db, user_id, order_number):
    db.execute("SELECT id, price FROM orders WHERE user_id = %s AND number = %s",
               (user_id, order_number))
    user_order = db.fetchone()
    return user_order


def update_order_status(db, user_id, order_number):
    db.execute(
        "UPDATE orders SET status ='paid' WHERE user_id = %s AND number = %s", (user_id, order_number))


def get_order_data_by_order_number(db, user_id, order_number):
    query_stat = "SELECT * FROM orders WHERE number = %s AND user_id = %s"
    params = (order_number, user_id)
    db.execute(query_stat, params)
    order = db.fetchone()
    return order
