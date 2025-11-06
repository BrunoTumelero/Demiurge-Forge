from fastapi import APIRouter, Response, status
from app.db.postgres import healthcheck as pg_ok, ensure_schema
from app.integrations.minio_client import healthcheck as s3_ok, ensure_bucket
from app.core.settings import settings

router = APIRouter()

@router.get("/healthz")
def healthz():
    return {"status": "ok"}

@router.get("/readyz")
def readyz():
    try:
        ensure_schema()
        ensure_bucket(settings.PDF_BUCKET)
        pg_ok()
        s3_ok()
        return {"ready": True}
    except Exception as e:
        return Response(content=str(e), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
