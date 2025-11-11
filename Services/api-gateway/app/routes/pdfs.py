import io, uuid, hashlib, os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.settings import settings
from app.integrations.minio_client import ensure_bucket, put_object
from app.db.postgres import insert_pdf
from app.schemas.pdf import PDFUploadResponse
from minio import Minio

router = APIRouter(prefix="/pdfs", tags=["PDFs"])

@router.get("/ping")
def ping():
    return {"ok": True}

@router.get("/conecta")
def conecta():
    client = Minio(
        "minio:9000",
        access_key='forge',
        secret_key='forge123',
        secure=False
    )
    buckets = [b.name for b in client.list_buckets()]
    return {
        "ok": True,
        "endpoint": "minio:9000",
        "buckets": buckets
    }

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    # aceita PDF "puro" e octet-stream (Postman às vezes manda assim)
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        print(1.1)
        raise HTTPException(status_code=415, detail="Envie um PDF")

    raw = await file.read()
    size = len(raw)
    if size == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio")
    if size > 100 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF muito grande (>100MB)")

    pdf_id  = str(uuid.uuid4())
    user_id = "u_demo"
    key     = f"pdfs/{user_id}/{pdf_id}.pdf"
    bucket  = getattr(settings, "PDF_BUCKET", os.getenv("PDF_BUCKET", "user-uploads"))

    try:
        ensure_bucket(bucket)
        # ATENÇÃO ao retorno do teu helper:
        # se ele retorna PutObjectResult, capture e use .etag
        result = put_object(bucket, key, io.BytesIO(raw), size, file.content_type)
        etag = getattr(result, "etag", result)  # se for string, mantém; se for objeto, pega .etag
    except Exception as e:
        # devolve detalhe pra facilitar debug (ajuste a verbosidade se quiser)
        raise HTTPException(status_code=500, detail=f"Erro no MinIO: {e}")

    sha256 = hashlib.sha256(raw).hexdigest()
    uri= f"s3://{bucket}/{key}"
    insert_pdf({
        "id": pdf_id,
        "user_id": user_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": size,
        "bucket": bucket,
        "storage_key": key,
        "storage_uri": uri,
        "etag": etag,
        "sha256": sha256,
        "status": "uploaded",
    })

    return PDFUploadResponse(
        pdf_id=pdf_id,
        filename=file.filename,
        size_bytes=size,
        storage_uri=uri,
        status="uploaded",
    )
