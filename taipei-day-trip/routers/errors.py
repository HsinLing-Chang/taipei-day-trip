from fastapi import APIRouter, HTTPException, status
router = APIRouter()


@router.get("/{full_path:path}")
def page_not_found(full_path: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Page was not found")
