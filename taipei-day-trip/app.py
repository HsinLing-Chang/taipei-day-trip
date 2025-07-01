from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from routers.user import auth
from routers import mrt, attractions, order, booking, errors


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(mrt.router)
app.include_router(attractions.router)
app.include_router(booking.router)
app.include_router(order.router)


@app.exception_handler(HTTPException)
def http_validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(content={"error": True, "message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
        "error": True,
        "message": exc.errors()
    })


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/html/index.html", media_type="text/html")


@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
    return FileResponse("./static/html/attraction.html", media_type="text/html")


@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
    return FileResponse("./static/html/booking.html", media_type="text/html")


@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
    return FileResponse("./static/html/thankyou.html", media_type="text/html")

app.include_router(errors.router)
