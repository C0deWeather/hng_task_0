from fastapi import APIRouter, HTTPException, status
from api.services import classify_name
from api.schemas import SuccessResponse

router = APIRouter()

@router.get("/get_health")
async def get_health():
    return {"status": "ok"}

@router.get("/api/classify", response_model=SuccessResponse)
async def classify(name: str):
    try:
        result = await classify_name(name)
        return SuccessResponse(status="success", data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
