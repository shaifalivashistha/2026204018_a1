CREATE MATERIALIZED VIEW mv_clinic_monthly_discharges AS
SELECT 
    c.id AS clinic_id,
    c.name AS clinic_name,
    DATE_TRUNC('month', a.created_at) AS month_year,
    COUNT(a.id) AS total_discharges
FROM clinics c
JOIN appointments a ON c.id = a.clinic_id
WHERE a.status = 'DISCHARGED'
GROUP BY c.id, c.name, DATE_TRUNC('month', a.created_at);

CREATE UNIQUE INDEX idx_mv_clinic_monthly ON mv_clinic_monthly_discharges (clinic_id, month_year);
