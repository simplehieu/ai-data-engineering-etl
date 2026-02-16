import requests
from src.utils import env, load_json_file

def extract_records():
    mode = env("INPUT_MODE", "file")

    if mode == "api":
        url = env("API_URL")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # default: file
    path = env("INPUT_FILE", "/opt/airflow/data/sample_input.json")
    return load_json_file(path)