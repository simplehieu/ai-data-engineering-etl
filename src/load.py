from src.utils import pg_conn

SCHEMA_SQL_PATH = "/opt/airflow/sql/schema.sql"
ANALYTICS_SQL_PATH = "/opt/airflow/sql/analytics.sql"

def init_schema():
    conn = pg_conn()
    try:
        with conn.cursor() as cur:
            with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
                cur.execute(f.read())
            with open(ANALYTICS_SQL_PATH, "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()
    finally:
        conn.close()

def load_records(data: dict):
    conn = pg_conn()
    try:
        with conn.cursor() as cur:
            for p in data["people"]:
                cur.execute(
                    """
                    INSERT INTO people (person_id, full_name, email, title, source, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (person_id) DO UPDATE SET
                      full_name=EXCLUDED.full_name,
                      email=EXCLUDED.email,
                      title=EXCLUDED.title,
                      source=EXCLUDED.source,
                      updated_at=EXCLUDED.updated_at
                    """,
                    (p["person_id"], p["full_name"], p["email"], p["title"], p["source"], p["updated_at"])
                )

            for o in data["organizations"]:
                cur.execute(
                    """
                    INSERT INTO organizations (org_id, org_name, domain, industry, source, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (org_id) DO UPDATE SET
                      org_name=EXCLUDED.org_name,
                      domain=EXCLUDED.domain,
                      industry=EXCLUDED.industry,
                      source=EXCLUDED.source,
                      updated_at=EXCLUDED.updated_at
                    """,
                    (o["org_id"], o["org_name"], o["domain"], o["industry"], o["source"], o["updated_at"])
                )

            for e in data["edges"]:
                cur.execute(
                    """
                    INSERT INTO person_org_edges (person_id, org_id, role, start_date, end_date, confidence)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (person_id, org_id, role) DO UPDATE SET
                      start_date=EXCLUDED.start_date,
                      end_date=EXCLUDED.end_date,
                      confidence=EXCLUDED.confidence
                    """,
                    (e["person_id"], e["org_id"], e["role"], e["start_date"], e["end_date"], e["confidence"])
                )

        conn.commit()
    finally:
        conn.close()