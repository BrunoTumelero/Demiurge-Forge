from minio import Minio
from app.core.settings import settings

_client = None

def client() -> Minio:
    global _client
    if _client is None:
        _client = Minio(
            settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_ENDPOINT.startswith("https"),
        )
    return _client

def healthcheck():
    # tenta listar buckets só pra validar credenciais/endpoint
    list(client().list_buckets())
    return True

def ensure_bucket(name: str):
    c = client()
    if not c.bucket_exists(name):
        c.make_bucket(name)

def put_object(bucket: str, key: str, data, length: int, content_type: str):
    res = client().put_object(bucket, key, data, length, content_type=content_type)
    return getattr(res, "etag", None)
