from fastapi import FastAPI
from fastapi.responses import JSONResponse
from storage import Entry, submit, exists

app = FastAPI(title="CyberCX Task API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/submit", response_class=JSONResponse)
async def submit(payload: Entry):
    try:
        submit(payload)
        return JSONResponse(content=hash(payload), status_code=201)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@app.get("/data")
async def data(payload: Entry):
    if exists(payload):
        return JSONResponse(content=payload.to_json(), status_code=200)
    else:
        return JSONResponse(content={"message": "Entry not found"}, status_code=404)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000)
