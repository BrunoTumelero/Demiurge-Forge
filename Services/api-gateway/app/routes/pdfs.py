import io, uuid, hashlib
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.settings import settings
from app.integrations.minio_client import ensure_bucket, put_object
from app.db.postgres import insert_pdf
from app.schemas.pdf import PDFUploadResponse

router = APIRouter(prefix="/pdfs", tags=["PDFs"])

@router.get("/ping")
def ping():
    return {"ok": True}

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Apenas application/pdf")

    raw = await file.read()
    size = len(raw)
    if size == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio")
    if size > 100 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF muito grande (>100MB)")

    pdf_id = str(uuid.uuid4())
    user_id = "u_demo"  # To-do: pegar do auth quando existir
    key = f"pdfs/{user_id}/{pdf_id}.pdf"
    bucket = settings.PDF_BUCKET
    ensure_bucket(bucket)

    etag = put_object(bucket, key, io.BytesIO(raw), size, file.content_type)
    sha256 = hashlib.sha256(raw).hexdigest()
    uri = f"s3://{bucket}/{key}"

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
