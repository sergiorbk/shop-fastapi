from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: int
    message: str
    status: str
    details: list[dict] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
