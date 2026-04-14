from fastapi import APIRouter, HTTPException, Query, status
from api.services import classify_name
from api.schemas import SuccessResponse

router = APIRouter()

@router.get("/get_health")
async def get_health():
    return {"status": "ok"}

@router.get("/api/classify", response_model=SuccessResponse)
async def classify(name: str = Query(..., min_length=1)):
    normalized_name = name.strip()
    if not normalized_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error",
        )
    try:
        result = await classify_name(normalized_name)
        return SuccessResponse(status="success", data=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
