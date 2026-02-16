CREATE TABLE IF NOT EXISTS people (
  person_id TEXT PRIMARY KEY,
  full_name TEXT NOT NULL,
  email TEXT,
  title TEXT,
  source TEXT,
  updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS organizations (
  org_id TEXT PRIMARY KEY,
  org_name TEXT NOT NULL,
  domain TEXT,
  industry TEXT,
  source TEXT,
  updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS person_org_edges (
  person_id TEXT NOT NULL REFERENCES people(person_id),
  org_id TEXT NOT NULL REFERENCES organizations(org_id),
  role TEXT NOT NULL,
  start_date DATE,
  end_date DATE,
  confidence DOUBLE PRECISION DEFAULT 0.9,
  PRIMARY KEY (person_id, org_id, role)
);