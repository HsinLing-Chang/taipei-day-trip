from typing import List, Optional
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, field_validator
import mysql.connector
import json
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

PASSWORD = os.getenv("PASSWORD")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")

user_config = {
    "user": USER,
    "password": PASSWORD,
    "host": HOST,
    "database": DB_NAME,
}


@app.exception_handler(HTTPException)
def validation_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 500:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)
    if exc.status_code == 400:
        return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)


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

    @field_validator("description")
    @classmethod
    def trunc_description(cls, v):
        maxlength = 50
        return v[:50] + "..." if len(v) > maxlength else v


class api_response(BaseModel):
    nextPage: int | None
    data: List[attraction_response]


class attraction_id_response(BaseModel):
    data: attraction_response


class mrt_response(BaseModel):
    data: List[str]


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
        sql_query += " GROUP BY attractions.id LIMIT 12 OFFSET %s "
        params.extend([OFFSET])

        db.execute(sql_query, tuple(params))
        data = db.fetchall()

        for row in data:
            row["images"] = json.loads(row.get("images"))

        db.execute(
            "SELECT COUNT(*) AS count FROM attractions")
        total_date = db.fetchone()

        next_page = None if total_date.get(
            "count") < 12*(page+1) or not data else (page + 1)

        return {"nextPage": next_page, "data": data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
