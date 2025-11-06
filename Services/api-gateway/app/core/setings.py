import os

class Settings:
    POSTGRES_URL = os.getenv("POSTGRES_URL")  # ex: postgresql://user:pass@postgres:5432/demiurge
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    PDF_BUCKET = os.getenv("PDF_BUCKET", "pdfs")

settings = Settings()
