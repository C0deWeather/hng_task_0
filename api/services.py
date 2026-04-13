import httpx
from datetime import datetime
from fastapi import HTTPException
from api.schemas import ClassificationResult, ExternalAPIResponse

async def fetch_data_from_api(name: str):
    url = f"https://api.genderize.io?name={name}"
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
            detail="Connection failed"
        )

async def classify_name(name: str) -> ClassificationResult:
    api_response = await fetch_data_from_api(name)
    if api_response.count == 0 or api_response.gender is None:
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
        processed_at=datetime.now(datetime.timezone.utc))