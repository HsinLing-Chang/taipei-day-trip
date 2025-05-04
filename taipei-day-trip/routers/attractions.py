from fastapi import APIRouter, Depends, Query, HTTPException, status
from dependencies.db import get_db
from repositories.attractions_repository import fetch_attractions_by_page, fetch_attraction_by_id
import json

router = APIRouter(prefix="/api", tags=['Attractions'])


@router.get("/attractions")
def get_attractions(page: int = Query(ge=0), keyword: str = None, db=Depends(get_db)):
    try:
        data = fetch_attractions_by_page(db, page, keyword)
        has_next_page = len(data) > 12
        next_page = (page + 1) if has_next_page else None
        data = data[:12] if has_next_page else data

        for row in data:
            row["images"] = json.loads(row.get("images"))

        return {"nextPage": next_page, "data": data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="伺服器錯誤，請稍後再嘗試")


@router.get("/attraction/{attraction_id}")
def get_attraction_by_id(attraction_id: int,  db=Depends(get_db)):
    try:
        attraction = fetch_attraction_by_id(db, attraction_id)
        if not attraction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="景點編號不正確")
        attraction["images"] = json.loads(attraction.get("images"))
        return {"data": attraction}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
