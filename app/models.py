from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    """Request model for calculator operations"""
    num1: float = Field(..., description="First number")
    num2: float = Field(..., description="Second number")


class OperationResponse(BaseModel):
    """Response model for calculator operations"""
    result: float = Field(..., description="Result of the operation")
    operation: str = Field(..., description="Operation performed")
