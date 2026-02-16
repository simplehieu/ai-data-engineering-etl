def validate_records(data: dict) -> None:
    people = data.get("people", [])
    orgs = data.get("organizations", [])
    edges = data.get("edges", [])

    # Required fields checks
    for p in people:
        if not p.get("person_id") or not p.get("full_name"):
            raise ValueError(f"Invalid person record: {p}")

    for o in orgs:
        if not o.get("org_id") or not o.get("org_name"):
            raise ValueError(f"Invalid organization record: {o}")

    # Dedupe checks
    person_ids = [p["person_id"] for p in people]
    org_ids = [o["org_id"] for o in orgs]
    if len(set(person_ids)) != len(person_ids):
        raise ValueError("Duplicate person_id detected.")
    if len(set(org_ids)) != len(org_ids):
        raise ValueError("Duplicate org_id detected.")

    # Edge consistency
    person_set = set(person_ids)
    org_set = set(org_ids)
    for e in edges:
        if e["person_id"] not in person_set:
            raise ValueError(f"Edge references unknown person_id: {e}")
        if e["org_id"] not in org_set:
            raise ValueError(f"Edge references unknown org_id: {e}")