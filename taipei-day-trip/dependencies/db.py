from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv()


PASSWORD = os.getenv("PASSWORD")
DB_USER = os.getenv("DB_USER")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")

user_config = {
    "user": DB_USER,
    "password": PASSWORD,
    "host": HOST,
    "database": DB_NAME,
}


def get_db():
    cnx = mysql.connector.connect(**user_config)
    cursor = cnx.cursor(dictionary=True)
    try:
        yield cursor
        cnx.commit()
    finally:
        cursor.close()
        cnx.close()
