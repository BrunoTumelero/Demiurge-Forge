from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.pdfs import router as pdfs_router

app = FastAPI(title="Demiurge Forge API", version="0.1.0")

app.include_router(health_router, tags=["health"])
app.include_router(pdfs_router, prefix="/v1", tags=["pdfs"])


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
