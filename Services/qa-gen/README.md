# qa-gen
Gera e valida perguntas usando IA.

Fluxo:
1. Recebe `chunk_ids` ou `qa.generate`
2. Recupera texto base (Postgres/Qdrant)
3. Gera perguntas + respostas via LLM
4. Valida se resposta está suportada no texto
5. Deduplica e salva
6. Emite `qa.questions_ready`
