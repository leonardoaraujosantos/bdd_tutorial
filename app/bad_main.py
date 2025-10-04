"""
BAD API IMPLEMENTATION - This passes BDD tests but has terrible code quality
DO NOT USE IN PRODUCTION!
"""

from fastapi import FastAPI
from app.models import OperationRequest, OperationResponse
from app.bad_calculator import BadCalculator

# BAD PRACTICE: No configuration management, hardcoded values
app = FastAPI(
    title="Bad Calculator API",
    description="An insecure calculator API - DO NOT USE!",
    version="0.1.0"
)

# BAD PRACTICE: Creating global instance - not thread-safe
calculator = BadCalculator()


@app.get("/")
async def root():
    """Health check - this one is OK"""
    return {"message": "Calculator API is running"}


@app.post("/add", response_model=OperationResponse)
async def add(request: OperationRequest):
    """
    BAD: This works for BDD but uses insecure eval internally
    """
    # The BDD test will pass because the result is correct
    # But internally it uses dangerous eval()
    result = calculator.add(request.num1, request.num2)
    return OperationResponse(result=result, operation="addition")


@app.post("/subtract", response_model=OperationResponse)
async def subtract(request: OperationRequest):
    """
    BAD: Uses exec() internally - major security issue
    """
    result = calculator.subtract(request.num1, request.num2)
    return OperationResponse(result=result, operation="subtraction")


@app.post("/multiply", response_model=OperationResponse)
async def multiply(request: OperationRequest):
    """
    BAD: Uses shell command injection vulnerability
    """
    result = calculator.multiply(request.num1, request.num2)
    return OperationResponse(result=result, operation="multiplication")


@app.post("/divide", response_model=OperationResponse)
async def divide(request: OperationRequest):
    """
    BAD: Poor error handling, returns string on error
    """
    result = calculator.divide(request.num1, request.num2)

    # BAD PRACTICE: Type checking at runtime instead of proper error handling
    if result == "Error":
        # BAD PRACTICE: Returning success status with error in body
        return OperationResponse(result=0, operation="division_error")

    return OperationResponse(result=result, operation="division")
