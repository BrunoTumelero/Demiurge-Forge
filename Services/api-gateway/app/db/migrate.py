from app.db.postgres import get_conn
from pathlib import Path


def run_migrations():
    migrations_path = Path(__file__).parent / "migrations"
    sql_files = sorted(migrations_path.glob("*.sql"))
    with get_conn() as conn:
        with conn.cursor() as cur:
            for file in sql_files:
                print(f"🗂️ Executando migração: {file.name}")
                cur.execute(file.read_text())
            conn.commit()
    print("✅ Todas as migrações foram aplicadas com sucesso")