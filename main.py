from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from storage import Entry, search, submit, exists
from validation import DataRequest

app = FastAPI(title="CyberCX Task API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/submit", response_class=JSONResponse)
async def submit_endpoint(entry: Entry):
    try:
        submit(entry)
        return JSONResponse(content=hash(entry), status_code=201)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@app.get("/data")
async def data_endpoint(request: DataRequest):
    try:
        return JSONResponse(content=search(request))
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000)
