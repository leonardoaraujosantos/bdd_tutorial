from fastapi import FastAPI, HTTPException
from app.models import OperationRequest, OperationResponse
from app.calculator import Calculator

app = FastAPI(
    title="Calculator API",
    description="A simple calculator API with basic arithmetic operations",
    version="1.0.0"
)

calculator = Calculator()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Calculator API is running"}


@app.post("/add", response_model=OperationResponse)
async def add(request: OperationRequest):
    """Add two numbers"""
    result = calculator.add(request.num1, request.num2)
    return OperationResponse(result=result, operation="addition")


@app.post("/subtract", response_model=OperationResponse)
async def subtract(request: OperationRequest):
    """Subtract two numbers"""
    result = calculator.subtract(request.num1, request.num2)
    return OperationResponse(result=result, operation="subtraction")


@app.post("/multiply", response_model=OperationResponse)
async def multiply(request: OperationRequest):
    """Multiply two numbers"""
    result = calculator.multiply(request.num1, request.num2)
    return OperationResponse(result=result, operation="multiplication")


@app.post("/divide", response_model=OperationResponse)
async def divide(request: OperationRequest):
    """Divide two numbers"""
    result = calculator.divide(request.num1, request.num2)
    return OperationResponse(result=result, operation="division")
