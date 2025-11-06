import psycopg
from app.core.settings import settings

DDL = """
CREATE TABLE IF NOT EXISTS pdfs (
  id UUID PRIMARY KEY,
  user_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  content_type TEXT NOT NULL,
  size_bytes BIGINT NOT NULL,
  bucket TEXT NOT NULL,
  storage_key TEXT NOT NULL,
  storage_uri TEXT NOT NULL,
  etag TEXT,
  sha256 TEXT,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
"""

def get_conn():
    return psycopg.connect(settings.POSTGRES_URL)

def healthcheck():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return True

def ensure_schema():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
            conn.commit()

def insert_pdf(row: dict):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO pdfs
                (id,user_id,filename,content_type,size_bytes,bucket,storage_key,storage_uri,etag,sha256,status)
                VALUES (%(id)s,%(user_id)s,%(filename)s,%(content_type)s,%(size_bytes)s,%(bucket)s,%(storage_key)s,%(storage_uri)s,%(etag)s,%(sha256)s,%(status)s);""",
                row,
            )
            conn.commit()
