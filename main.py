from typing import Annotated
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import storage
from validation import DataParams, StorageEntry

app = FastAPI(title="CyberCX Task API", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with detailed error messages"""
    errors = [
        {
            "field": " -> ".join(
                str(loc) for loc in error["loc"][1:]  # `[1:]` so we skip the `body` key
            ),
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input"),
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": errors,
            "detail": "One or more fields failed validation",
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/submit", response_class=JSONResponse)
async def submit(entry: StorageEntry):
    try:
        storage.submit(entry)
        return JSONResponse(content=hash(entry), status_code=201)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@app.get("/data", response_class=JSONResponse)
async def data(params: Annotated[DataParams, Query()]):
    try:
        results = storage.search(params.q, params.limit, params.tags)
        return JSONResponse(content=[result.model_dump() for result in results])
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000)
