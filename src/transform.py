from datetime import datetime

def _norm(s: str):
    return (s or "").strip()

def transform_records(payload: dict) -> dict:
    # Expected payload format:
    # { "people": [...], "organizations": [...], "edges": [...] }
    people = payload.get("people", [])
    orgs = payload.get("organizations", [])
    edges = payload.get("edges", [])

    now = datetime.utcnow().isoformat()

    people_out = []
    for p in people:
        people_out.append({
            "person_id": _norm(p.get("person_id")),
            "full_name": _norm(p.get("full_name")),
            "email": _norm(p.get("email")),
            "title": _norm(p.get("title")),
            "source": _norm(p.get("source", "sample")),
            "updated_at": p.get("updated_at", now),
        })

    orgs_out = []
    for o in orgs:
        orgs_out.append({
            "org_id": _norm(o.get("org_id")),
            "org_name": _norm(o.get("org_name")),
            "domain": _norm(o.get("domain")),
            "industry": _norm(o.get("industry")),
            "source": _norm(o.get("source", "sample")),
            "updated_at": o.get("updated_at", now),
        })

    edges_out = []
    for e in edges:
        edges_out.append({
            "person_id": _norm(e.get("person_id")),
            "org_id": _norm(e.get("org_id")),
            "role": _norm(e.get("role")),
            "start_date": e.get("start_date"),
            "end_date": e.get("end_date"),
            "confidence": float(e.get("confidence", 0.9)),
        })

    return {"people": people_out, "organizations": orgs_out, "edges": edges_out}