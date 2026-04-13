from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class ExternalAPIResponse(BaseModel):
    count: int
    name: str
    gender: str
    probability: float


class ClassificationResult(BaseModel):
    name: str
    gender: str
    probability: float
    sample_size: int
    is_confident: bool
    processed_at: datetime


class SuccessResponse(BaseModel):
    status: Literal["success"]
    data: ClassificationResult


class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str
