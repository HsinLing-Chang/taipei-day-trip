from typing import List, Optional
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator
from fastapi.staticfiles import StaticFiles
import mysql.connector
from datetime import datetime, timezone, timedelta
import json
import re
import os
import jwt
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

PASSWORD = os.getenv("PASSWORD")
DB_USER = os.getenv("DB_USER")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")

user_config = {
    "user": DB_USER,
    "password": PASSWORD,
    "host": HOST,
    "database": DB_NAME,
}


@app.exception_handler(HTTPException)
def http_validation_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 500:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=500)
    if exc.status_code == 400:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)
    if exc.status_code == 403:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)
    if exc.status_code == 404:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
        "error": True,
        "message": exc.errors()
    })


def verifytoken_wrapper(return_none: bool = False):
    def verify_token(authorization: Optional[str] = Header(None)):
        try:
            if not authorization or not authorization.startswith("Bearer"):
                if return_none:
                    return None
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invaild or missing token")
            token = authorization.split(" ")[1]
            userDate = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            return userDate
        except jwt.ExpiredSignatureError as e:
            if return_none:
                return None
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
        except jwt.exceptions.PyJWTError as e:
            if return_none:
                return None
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return verify_token


def get_db():
    cnx = mysql.connector.connect(**user_config)
    cursor = cnx.cursor(dictionary=True)
    try:
        yield cursor
        cnx.commit()
    finally:
        cursor.close()
        cnx.close()


class attraction_response(BaseModel):
    id: int
    name: str
    category: str
    description: str
    address: str
    transport: str
    mrt: Optional[str] = None
    lat: float
    lng: float
    images: List[str] = None

    # @field_validator("description")
    # @classmethod
    # def trunc_description(cls, v):
    #     maxlength = 50
    #     return v[:50] + "..." if len(v) > maxlength else v


class api_response(BaseModel):
    nextPage: int | None
    data: List[attraction_response]


class attraction_id_response(BaseModel):
    data: attraction_response


class mrt_response(BaseModel):
    data: List[str]


class sign_up_form(BaseModel):
    name: str = Field(...)
    email:  str = Field(...)
    password: str = Field(...)


class sing_in_form(BaseModel):
    email:  str = Field(...)
    password: str = Field(...)


class booking_form_validator(BaseModel):
    attractionID: int
    date: str
    time: str
    price: int

    @validator("date")
    def validate_dates(cls, val):
        regex1 = r'\d{4}-\d{2}-\d{2}'
        if not re.match(regex1, val):
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

# Static Pages (Never Modify Code in this Block)


@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")


@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
    return FileResponse("./static/attraction.html", media_type="text/html")


@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
    return FileResponse("./static/booking.html", media_type="text/html")


@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
    return FileResponse("./static/thankyou.html", media_type="text/html")


# api
@app.get("/api/attractions", response_model=api_response)
def get_attractions(page: int = Query(ge=0), keyword: str = None, db=Depends(get_db)):
    try:
        OFFSET = 12*(page)
        next_page = page + 1
        sql_query = """
        SELECT attractions.id, attractions.name, attractions.category, attractions.description, attractions.address, attractions.transport, attractions.mrt, attractions.lat, attractions.lng,
        JSON_ARRAYAGG(img_urls.url) AS images
        FROM attractions
        INNER JOIN img_urls ON attractions.id = img_urls.attraction_id

        """
        conditions = []
        params = []
        if keyword:
            conditions.append(
                "WHERE attractions.mrt = %s OR attractions.name LIKE %s")
            params.extend([keyword, f"%{keyword}%"])
        if conditions:
            sql_query += " AND ".join(conditions)
        sql_query += " GROUP BY attractions.id LIMIT 13 OFFSET %s"
        params.extend([OFFSET])

        db.execute(sql_query, tuple(params))
        data = db.fetchall()

        next_page = (page + 1) if len(data) > 12 else None
        data = data[:-1] if len(data) > 12 else data

        for row in data:
            row["images"] = json.loads(row.get("images"))

        # db.execute(
        #     "SELECT COUNT(*) AS count FROM attractions")
        # total_date = db.fetchone()  total_date.get("count") < 12*(page+1)

        # next_page = None if len(data) < 12 or  not data else (page + 1)

        return {"nextPage": next_page, "data": data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="伺服器錯誤，請稍後再嘗試")


@app.get("/api/attraction/{attractionId}", response_model=attraction_id_response)
def get_attraction_by_id(attractionId: int, request: Request, db=Depends(get_db)):
    try:
        sql_query = """
        SELECT attractions.id, attractions.name, attractions.category, attractions.description, attractions.address, attractions.transport, attractions.mrt, attractions.lat, attractions.lng,
        JSON_ARRAYAGG(img_urls.url) AS images
        FROM attractions
        INNER JOIN img_urls ON attractions.id = img_urls.attraction_id
        WHERE attractions.id = %s
        GROUP BY attractions.id
        """
        db.execute(sql_query, (attractionId,))
        attraction = db.fetchone()
        if not attraction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="景點編號不正確")
        attraction["images"] = json.loads(attraction.get("images"))
        return {"data": attraction}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/mrts", response_model=mrt_response)
def get_mrt_stations(request: Request, db=Depends(get_db)):
    try:
        db.execute(
            "SELECT mrt, COUNT(mrt) AS count FROM attractions WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count DESC")
        res = db.fetchall()
        mrt_stations = [item.get("mrt") for item in res]
        return {"data": mrt_stations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/user")
def sign_up(formData: sign_up_form, db=Depends(get_db)):
    try:
        db.execute("SELECT email FROM member WHERE email = %s",
                   (formData.email,))
        email = db.fetchone()
        if email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="帳號已被註冊，請重新嘗試")
        db.execute("INSERT INTO member(name, email, password) VALUES (%s, %s, %s)",
                   (formData.name, formData.email, formData.password))
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/api/user/auth")
def sign_in(formDate: sing_in_form, db=Depends(get_db)):
    try:
        db.execute("SELECT id, name, email FROM member WHERE email = %s AND password = %s",
                   (formDate.email, formDate.password))
        user_data = db.fetchone()
        if user_data:
            expire_time = datetime.now(tz=timezone.utc) + timedelta(days=7)
            payload = {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "exp": expire_time
            }
            token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            return {"token": token}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="帳號或密碼錯誤，請重新嘗試。")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/user/auth")
def get_user(user_data=Depends(verifytoken_wrapper(return_none=True))):
    try:
        if user_data:
            return {"data": user_data}
        return {"data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# booking routes
@app.post("/api/booking")
def booking(booking_form: booking_form_validator, db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    try:
        id = user_data.get("id")
        params = (booking_form.attractionID, booking_form.date,
                  booking_form.time, booking_form.price, id)
        if id:
            db.execute(
                "SELECT * FROM booking WHERE user_id = %s", (id,))
            res = db.fetchone()
            if res:
                update_query = "UPDATE booking set attractionID = %s,  booking_date = %s, time = %s, price= %s WHERE user_id = %s"
                db.execute(update_query, params)
            else:
                db.execute(
                    "INSERT INTO booking (attractionID, booking_date, time, price, user_id) VALUES(%s,%s,%s,%s,%s)", params)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/booking")
def get_booking(db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    try:
        id = user_data.get("id")
        db.execute(
            "SELECT attractionID, booking_date, time, price FROM booking WHERE user_id = %s", (id,))
        booking_data = db.fetchone()
        if booking_data:
            db.execute(" SELECT a.id, name, address, url AS image FROM attractions a JOIN img_urls i ON a.id = i.attraction_id WHERE a.id = %s LIMIT 1;", (
                booking_data.get("attractionID"),))
            attraction = db.fetchone()
            return {"data": {
                "attraction": attraction,
                "date": booking_data.get("booking_date"),
                "time": booking_data.get("time"),
                "price": booking_data.get("price")
            }}
        else:
            return {"data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/api/booking")
def delete_booking(request: Request, db=Depends(get_db), user_data=Depends(verifytoken_wrapper())):
    try:
        id = user_data.get("id")
        db.execute("DELETE FROM booking WHERE user_id = %s", (id,))
        return {"ok": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/{full_path:path}")
def page_not_found(full_path: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Page was not found")
