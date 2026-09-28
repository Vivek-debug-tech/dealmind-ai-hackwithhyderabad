from fastapi import FastAPI
from .routes import memory, prepare

app = FastAPI(title="DealMind AI Backend")

app.include_router(memory.router, prefix="/api/memory", tags=["memory"])
app.include_router(prepare.router, prefix="/api/prepare", tags=["prepare"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
