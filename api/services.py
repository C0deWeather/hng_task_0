import httpx
from datetime import datetime, timezone
from fastapi import HTTPException
from api.schemas import ClassificationResult, ExternalAPIResponse
from api.config import settings

async def fetch_data_from_api(name: str):
    url = f"{settings.genderise_api}?name={name}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return ExternalAPIResponse(**response.json())

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=502,
            detail="External API request timed out"
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=502,
            detail="External API connection failed"
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"External API error: {exc.response.status_code}"
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"External API request error: {str(exc)}"
        )

async def classify_name(name: str) -> ClassificationResult:
    api_response = await fetch_data_from_api(name)
    if (
        api_response.count is None
        or api_response.gender is None
        or api_response.probability is None
        or api_response.name is None
    ):
        raise HTTPException(
            status_code=502,
            detail="Invalid response from external API"
        )
    if api_response.count == 0:
        raise HTTPException(
            status_code=404,
            detail="Name not found"
        )
    is_confident = (
        api_response.probability >= 0.7
        and api_response.count >= 100
    )
    return ClassificationResult(
        name=api_response.name,
        gender=api_response.gender,
        probability=api_response.probability,
        sample_size=api_response.count,
        is_confident=is_confident,
        processed_at=datetime.now(timezone.utc)
    )
