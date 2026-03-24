import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from fastapi import FastAPI

from api import v1_router
from core import setup_logging

setup_logging()

app = FastAPI(title="Todo Service")

app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
