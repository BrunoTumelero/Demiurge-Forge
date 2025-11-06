Visão geral

Serviços (contêineres):

Postgres — banco relacional (estado principal).

Redis — cache/filas leves e locks.

Qdrant — banco vetorial (similaridade semântica).

MinIO — storage S3-compatível para PDFs e artefatos.

API Gateway — porta de entrada HTTP da aplicação (healthcheck por enquanto).

Rede: internal (bridge Docker; serviços se enxergam por nome do serviço).
Volumes: dados persistentes de Postgres, Qdrant e MinIO (não se perdem ao remover contêiner).

Browser ──> API Gateway (:8000)
                │     ├── PostgreSQL (host: postgres:5432)
                │     ├── Redis     (host: redis:6379)
                │     ├── Qdrant    (host: qdrant:6333)
                │     └── MinIO     (host: minio:9000)
          (rede Docker: internal)


1) PostgreSQL (postgres)

Imagem: postgres:16

Por que existe: armazena usuários, PDFs registrados, chunks, perguntas, cards SRS e revisões.

Persistência: volume postgres-data montado em /var/lib/postgresql/data.

Portas (dev): 5433:5432 (host:container) – evita conflito com Postgres local.

Healthcheck: pg_isready -U $POSTGRES_USER -d $POSTGRES_DB

Conectar (host): localhost:5433 (DBeaver/psql)

Conectar (rede Docker): postgres:5432

2) Redis (redis)

Imagem: redis:7-alpine

Por que existe: cache e estruturas temporárias (ex.: rate-limit, locks) e/OU orquestração simples via pub/sub.

Persistência: não (dev). Em prod, considere snapshotting.

Portas: não expostas (acesso só pela rede interna).

Healthcheck: redis-cli ping ⇒ espera PONG.

Host interno: redis:6379

3) Qdrant (qdrant)

Imagem: qdrant/qdrant:latest (fixe tag em prod)

Por que existe: banco vetorial para recuperar chunks por similaridade (RAG).

Persistência: volume qdrant-data em /qdrant/storage.

Portas (dev): 6333:6333 para testar via cURL/insomnia.

Healthcheck: GET http://localhost:6333/ready

Host interno: qdrant:6333

4) MinIO (minio)

Imagem: minio/minio:latest (fixe tag em prod)

Por que existe: storage S3-compatível para arquivos PDF e saídas (exports, snapshots).

Persistência: volume minio-data em /data.

Portas (dev): 9000:9000 (S3 API), 9001:9001 (console web).

Credenciais (dev): MINIO_ROOT_USER, MINIO_ROOT_PASSWORD.

Healthcheck: GET /minio/health/ready

Host interno: minio:9000

5) API Gateway (api-gateway)

Imagem: build local (services/api-gateway/Dockerfile)

Por que existe: porta HTTP para upload, sessões de estudo, endpoints de controle.
No dev inicial, só /healthz.

Portas (dev): ${API_PORT}:8000 (ex.: 8000:8000)

Healthcheck: GET http://localhost:8000/healthz

Dependências: espera Postgres/Redis/Qdrant/MinIO ficarem healthy (Compose depends_on com condition).

Hosts internos usados pela API:

DB: postgres:5432

Redis: redis:6379

Qdrant: qdrant:6333

MinIO: minio:9000

Redes e Volumes

Rede

networks:
  internal:
    driver: bridge


Todos os serviços estão em internal. Eles se resolvem por DNS interno (nome do serviço).

Volumes

volumes:
  postgres-data: {}  # estado do banco relacional
  qdrant-data:   {}  # índice vetorial
  minio-data:    {}  # objetos (PDFs/artefatos)


Remover os volumes apaga dados (dev): docker compose down -v

Comandos úteis

# subir/derrubar
docker compose up -d
docker compose down

# reconstruir imagens locais ao subir
docker compose up -d --build

# status e logs
docker compose ps
docker compose logs -f postgres
docker compose logs -f api-gateway

# executar dentro de um serviço
docker compose exec postgres bash
docker compose exec redis redis-cli ping

# validar YAML expandido (pega erros de sintaxe)
docker compose config
