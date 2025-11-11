

CREATE TABLE IF NOT EXISTS pdfs (
    id UUID PRIMARY KEY,
    user_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    content_type TEXT,
    size_bytes BIGINT,
    bucket TEXT,
    storage_key TEXT,
    storage_uri TEXT,
    etag TEXT,
    sha256 TEXT,
    status TEXT
);
