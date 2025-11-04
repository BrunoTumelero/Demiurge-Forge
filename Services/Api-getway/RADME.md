# api-gateway
Porta de entrada da plataforma Demiurge Forge.

Responsável por:
- Upload de PDFs
- Autenticação do usuário
- Endpoints públicos (/pdfs, /study/session, /study/review)
- Comunicação com os outros microsserviços via fila/eventos

Stack:
- FastAPI
- PostgreSQL (via libs/contracts)
- Redis (pub/sub de eventos)
