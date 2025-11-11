from pydantic import BaseModel

class PDFUploadResponse(BaseModel):
    pdf_id: str
    filename: str
    size_bytes: int
    storage_uri: str
    status: str
