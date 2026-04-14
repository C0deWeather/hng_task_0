from fastapi import APIRouter, HTTPException, Query, status
from api.services import classify_name
from api.schemas import ErrorResponse, SuccessResponse

router = APIRouter()

@router.get("/get_health")
async def get_health():
    return {"status": "ok"}

@router.get(
    "/api/classify",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Name not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        502: {"model": ErrorResponse, "description": "External API error"},
    },
)
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
