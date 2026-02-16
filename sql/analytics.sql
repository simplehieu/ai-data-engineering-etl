-- Example reporting views for dashboards / reporting features

CREATE OR REPLACE VIEW v_org_headcount AS
SELECT
  o.org_id,
  o.org_name,
  COUNT(DISTINCT e.person_id) AS people_count
FROM organizations o
LEFT JOIN person_org_edges e ON e.org_id = o.org_id
GROUP BY o.org_id, o.org_name
ORDER BY people_count DESC;

CREATE OR REPLACE VIEW v_people_roles AS
SELECT
  p.person_id,
  p.full_name,
  e.role,
  o.org_name,
  e.start_date,
  e.end_date,
  e.confidence
FROM person_org_edges e
JOIN people p ON p.person_id = e.person_id
JOIN organizations o ON o.org_id = e.org_id;