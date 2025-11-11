from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.pdfs import router as pdfs_router
import os

app = FastAPI(title="Demiurge Forge API", version="0.1.0")

app.include_router(health_router, tags=["health"])
app.include_router(pdfs_router, prefix="/v1", tags=["pdfs"])


@app.on_event("startup")
async def init_db():
    from app.db.migrate import run_migrations
    run_migrations()


@app.on_event("startup")
async def _show_routes():
    print("=== ROUTES REGISTRADAS ===")
    for r in app.router.routes:
        methods = getattr(r, "methods", None)
        print(methods, r.path)

@app.on_event("startup")
async def _env_debug():
    keys = ["MINIO_ENDPOINT","MINIO_ACCESS_KEY","MINIO_SECRET_KEY","S3_ENDPOINT",
            "S3_ACCESS_KEY","S3_SECRET_KEY","S3_SECURE","PDF_BUCKET", "POSTGRES_URL"]
    print("=== ENV SNAPSHOT ===")
    for k in keys:
        print(k, "=", os.getenv(k))