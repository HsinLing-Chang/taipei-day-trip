

def get_user_email(db, email: str):
    db.execute("SELECT email FROM member WHERE email = %s",
               (email,))
    email = db.fetchone()
    return email


def get_user_data_by_email(db, email):
    db.execute("SELECT id, name, email ,password FROM member WHERE email = %s",
               (email,))
    user_data = db.fetchone()
    return user_data


def create_user(db, name, email, password):
    db.execute("INSERT INTO member(name, email, password) VALUES (%s, %s, %s)",
               (name, email, password))
