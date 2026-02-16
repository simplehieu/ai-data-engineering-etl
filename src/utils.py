import os
import json
import psycopg2


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def load_json_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pg_conn():
    return psycopg2.connect(
        host=env("PG_HOST", "postgres"),
        port=int(env("PG_PORT", "5432")),
        dbname=env("PG_DB", "airflow"),
        user=env("PG_USER", "airflow"),
        password=env("PG_PASSWORD", "airflow"),
    )