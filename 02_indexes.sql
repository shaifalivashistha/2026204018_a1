CREATE UNIQUE INDEX idx_active_consult ON appointments (patient_id) 
WHERE status IN ('WAITING', 'IN_CONSULTATION');
