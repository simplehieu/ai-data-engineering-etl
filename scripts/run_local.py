#import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extract import extract_records
from src.transform import transform_records
from src.validate import validate_records
from src.load import init_schema, load_records

if __name__ == "__main__":
    # If running outside docker, set env vars as needed:
    # os.environ["PG_HOST"]="localhost"
    # os.environ["PG_PORT"]="5432"
    # os.environ["PG_DB"]="airflow"
    # os.environ["PG_USER"]="airflow"
    # os.environ["PG_PASSWORD"]="airflow"

    raw = extract_records()
    transformed = transform_records(raw)
    validate_records(transformed)
    init_schema()
    load_records(transformed)
    print("✅ Pipeline completed successfully.")