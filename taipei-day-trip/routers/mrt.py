from fastapi import APIRouter, Depends, HTTPException, status
from repositories.mrt_repository import fetch_mrt_stations
from dependencies.db import get_db
router = APIRouter(prefix="/api", tags=["MRT Station"])


@router.get("/mrts")
def get_mrt_stations(db=Depends(get_db)):
    try:
        mrts = fetch_mrt_stations(db)
        mrt_stations = [item.get("mrt") for item in mrts]
        return {"data": mrt_stations}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
