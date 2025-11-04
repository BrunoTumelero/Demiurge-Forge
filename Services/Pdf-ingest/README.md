# pdf-ingest
Serviço responsável por extrair texto, limpar e dividir PDFs em chunks.

Fluxo:
1. Recebe evento `pdf.submitted`
2. Extrai texto (OCR opcional)
3. Normaliza e limpa
4. Divide em chunks (~500 palavras)
5. Armazena chunks e envia embeddings ao Qdrant
6. Emite evento `ingest.chunks_ready`
