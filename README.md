# AI Data Engineering ETL Pipeline  
Airflow · PostgreSQL · Docker · Python  

A production-style data engineering pipeline that ingests semi-structured entity data, enforces data quality constraints, models relationships in a normalized relational schema, and exposes reporting views for downstream analytics.

This project demonstrates how to architect and deploy a modular, containerized ETL system designed for scalable relationship modeling — similar to systems used in talent intelligence, analytics, and knowledge graph platforms.

---

## 🎯 Project Overview

The pipeline processes structured JSON data describing:

- **People**
- **Organizations**
- **Professional relationships (edges)**

It performs:

1. Extraction from file or API
2. Field normalization and transformation
3. Validation (deduplication, required-field enforcement, referential integrity)
4. Upsert-based loading into PostgreSQL
5. Creation of reporting views for analytics

The system is orchestrated using **Apache Airflow** and deployed via **Docker** for reproducibility.

---

## 🏗 Architecture

### Extract
- Supports ingestion from:
  - Local JSON (`data/sample_input.json`)
  - External REST APIs
- Designed for easy extension to batch or streaming inputs

### Transform
- Standardizes and cleans entity attributes
- Normalizes identifiers
- Structures relationship edges (`person → organization`)
- Supports incremental upsert logic

### Validate
- Required-field enforcement
- Duplicate entity detection
- Referential integrity checks between entities and edges

### Load
- Writes to PostgreSQL using idempotent upsert logic
- Tables:
  - `people`
  - `organizations`
  - `person_org_edges`
- Builds reporting views for analytical queries

### Orchestration
- Airflow DAG coordinates full ETL lifecycle
- Designed for scheduled, repeatable execution

---

## 📊 Example Reporting Output

After running the DAG:

```sql
SELECT * FROM v_org_headcount;
 org_id | org_name         | people_count
--------+------------------+--------------
 o_001  | Nimbus Analytics |            2
 o_002  | Vertex Labs      |            1
(2 rows)
```
---

## 🐳 Quickstart

### Requirements
- Docker + Docker Compose

### Run the stack
```bash
git clone <YOUR_REPO_URL>
cd ai-data-engineering-etl
docker compose up --build
```
### Access Airflow UI
Open:
http://localhost:8080

Login Credentials:
Username: airflow
Password: airflow 

Enable and trigger the DAG:
etl_people_org_pipeline