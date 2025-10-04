import os
import logging
import sentry_sdk
from fastapi import FastAPI, HTTPException
from app.models import OperationRequest, OperationResponse
from app.calculator import Calculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Sentry
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        # Add data like request headers and IP for users
        send_default_pii=True,
        # Enable sending logs to Sentry
        enable_logs=True,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        # Set profile_session_sample_rate to 1.0 to profile 100% of sessions
        profile_session_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "1.0")),
        # Set profile_lifecycle to "trace" to automatically run profiler on transactions
        profile_lifecycle="trace",
    )
    logger.info("Sentry initialized successfully")
else:
    logger.warning("Sentry DSN not configured - error tracking disabled")

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
    try:
        result = calculator.divide(request.num1, request.num2)
        return OperationResponse(result=result, operation="division")
    except ValueError as e:
        logger.error(f"Division error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sentry-debug")
async def trigger_error():
    """
    Debug endpoint to test Sentry integration
    This will trigger an error that gets sent to Sentry
    """
    logger.info("Sentry debug endpoint called - triggering error")
    division_by_zero = 1 / 0
    return {"message": "This should not be reached"}


@app.get("/sentry-log-test")
async def test_logging():
    """
    Test endpoint to verify Sentry logging integration
    """
    sentry_sdk.logger.info('This is an info log message sent directly to Sentry')
    sentry_sdk.logger.warning('This is a warning message')
    logger.info('This info log will be sent to Sentry via Python logging')
    logger.warning('User attempted an operation')
    logger.error('This is a test error log')

    return {
        "message": "Logs sent to Sentry",
        "logs": [
            "Info log via sentry_sdk.logger",
            "Warning via sentry_sdk.logger",
            "Info via Python logging",
            "Warning via Python logging",
            "Error via Python logging"
        ]
    }
