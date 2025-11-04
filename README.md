# 🧠 Demiurge Forge — Plataforma de aprendizado com IA e repetição espaçada

O **Demiurge Forge** é uma plataforma modular que transforma PDFs em um sistema inteligente de aprendizado, combinando **IA**, **extração semântica** e **repetição espaçada (SRS)**.  
Cada parte do sistema é um microserviço independente, orquestrado em Docker.

---

## 🚀 Visão Geral

O objetivo do Demiurge Forge é permitir que qualquer pessoa envie um PDF e, automaticamente, receba **perguntas relevantes** e **planos de estudo personalizados**.  
O sistema aprende com o progresso do usuário e aplica o algoritmo **SM-2 / FSRS** para otimizar a memorização.

Fluxo resumido:
1. O usuário envia um PDF.  
2. O sistema extrai e limpa o texto.  
3. IA gera perguntas com base nos trechos do conteúdo.  
4. O motor de SRS cria cartões e organiza sessões de estudo.  
5. A interface exibe as perguntas no ritmo ideal de aprendizado.

---

## 🧩 Arquitetura de Microsserviços

/services
├─ api-gateway → Porta de entrada da aplicação (FastAPI)
├─ orchestrator → Coordena e agenda os jobs e eventos
├─ pdf-ingest → Extrai texto, limpa e divide o PDF em chunks
├─ qa-gen → IA de geração e validação de perguntas
├─ srs-engine → Algoritmo SM-2 / FSRS e gestão da fila de estudo
├─ ui-web → Interface web (Next.js ou Streamlit)
/libs
├─ contracts → Schemas Pydantic (eventos, DTOs, erros)
├─ srs_core → Implementação pura do SRS (compartilhada)
├─ pdf_pipeline → Funções de parsing e chunking reutilizáveis
/infra
├─ docker-compose.yml
├─ postgres / redis / qdrant / minio / traefik
├─ prometheus / grafana / loki (monitoramento)
/scripts
├─ seed_data.py
├─ backup_restore.sh


---

## 🧠 Descrição dos Serviços

### **api-gateway**
- Recebe requisições do usuário final.
- Endpoints públicos (`/pdfs`, `/study/session`, `/study/review`, `/configs`).
- Salva uploads no **MinIO** e publica eventos para a fila.

### **orchestrator**
- Controla o fluxo do pipeline.
- Agenda jobs e distribui para os serviços certos (via Redis Streams).
- Implementa lógica de *retry*, *backoff* e *dead-letter queues*.

### **pdf-ingest**
- Faz parsing, limpeza e **chunking** dos PDFs.
- Extrai metadados (páginas, seções, tópicos).
- Gera **embeddings** e indexa no **Qdrant**.
- Emite evento `ingest.chunks_ready`.

### **qa-gen**
- Gera perguntas e respostas baseadas em contexto usando LLM.
- Valida coerência (a resposta precisa estar suportada no trecho).
- Elimina duplicatas e grava no banco.
- Emite `qa.questions_ready`.

### **srs-engine**
- Implementa o algoritmo de repetição espaçada (**SM-2 / FSRS**).
- Mantém o estado de cada cartão (intervalo, facilidade, acertos).
- Monta sessões diárias e registra revisões.

### **ui-web**
- Interface principal do usuário.
- Permite enviar PDFs, estudar e ajustar configurações pessoais.
- Comunicação 100% via `api-gateway`.

---

## ⚙️ Infraestrutura

- **Banco de Dados**: PostgreSQL  
- **Cache / Fila**: Redis  
- **Busca Vetorial**: Qdrant  
- **Armazenamento**: MinIO (compatível com S3)  
- **Proxy / HTTPS**: Traefik ou Caddy  
- **Observabilidade**: Prometheus + Grafana + Loki  

Cada serviço roda em seu próprio contêiner, com volumes dedicados e healthchecks.

---

## 🔄 Eventos Internos

| Evento | Origem | Ação |
|--------|--------|------|
| `pdf.submitted` | api-gateway | novo PDF recebido |
| `ingest.chunks_ready` | pdf-ingest | chunks processados e indexados |
| `qa.generate` | orchestrator | dispara geração de perguntas |
| `qa.questions_ready` | qa-gen | perguntas validadas e gravadas |
| `srs.daily_build` | orchestrator | cria fila diária de estudo |
| `srs.review_recorded` | api-gateway | usuário respondeu uma pergunta |

---

## 📦 Banco de Dados (modelo resumido)

| Tabela | Descrição |
|--------|------------|
| `users` | contas e permissões |
| `user_configs` | preferências e políticas do usuário |
| `pdfs` | PDFs enviados, status e hashes |
| `chunks` | trechos extraídos e limpos |
| `questions` | perguntas geradas pela IA |
| `cards` | estado do estudo (SRS) |
| `reviews` | histórico de respostas |
| `audit_logs` | ações do sistema e do usuário |

---

## ⚙️ Configurações do Usuário

O usuário tem acesso a uma área de **Configurações**, que substitui o painel “admin” clássico.

**Preferências principais**
- Novos cartões por dia  
- Duração média de sessão  
- Retenção alvo (ex.: 90%)  
- Mistura de tipos de pergunta  
- Idioma / estilo de IA  
- Política de privacidade e uso de dados  

**Avançadas (para power users)**
- Parâmetros de geração de perguntas  
- Modo de validação (estrito/laxo)  
- Deduplicação e sensibilidade semântica  
- Limites de coleção e reprocessamento  

---

## 🧱 Setup local

**Pré-requisitos**
- Docker + Docker Compose  
- Python 3.12+  
- Node.js (para a interface, se usar Next.js)

**Rodando o projeto**
```bash
docker compose up
