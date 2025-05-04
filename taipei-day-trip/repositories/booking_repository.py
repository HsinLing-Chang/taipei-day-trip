def fetch_bookinig_attraction(db, id):
    db.execute(
        "SELECT attractionID, booking_date, time, price FROM booking WHERE user_id = %s", (id,))
    booking_data = db.fetchone()
    return booking_data


def fetch_booking_record(db, id):
    db.execute(
        "SELECT 1 FROM booking WHERE user_id = %s", (id,))
    exists = db.fetchone()
    return exists


def update_booking_data(db, booking_form, user_id):
    params = (booking_form.attractionID, booking_form.date,
              booking_form.time, booking_form.price, user_id)
    update_query = "UPDATE booking set attractionID = %s,  booking_date = %s, time = %s, price= %s WHERE user_id = %s"
    db.execute(update_query, params)


def create_booking_data(db, booking_form, user_id):
    params = (booking_form.attractionID, booking_form.date,
              booking_form.time, booking_form.price, user_id)
    db.execute(
        "INSERT INTO booking (attractionID, booking_date, time, price, user_id) VALUES(%s,%s,%s,%s,%s)", params)


def delete_booking_data(db, user_id):
    db.execute("DELETE FROM booking WHERE user_id = %s", (user_id,))
