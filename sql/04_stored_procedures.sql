CREATE OR REPLACE PROCEDURE sp_execute_appointment(
    p_patient_id INT,
    p_clinic_id INT,
    p_copay DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_curr_balance DECIMAL(10,2);
BEGIN
    SELECT hsa_balance INTO v_curr_balance FROM patients WHERE id = p_patient_id FOR UPDATE;
    IF v_curr_balance IS NULL THEN RAISE EXCEPTION 'Patient ID % not found', p_patient_id; END IF;
    IF v_curr_balance < p_copay THEN RAISE EXCEPTION 'Insufficient HSA Balance'; END IF;
    UPDATE patients SET hsa_balance = hsa_balance - p_copay WHERE id = p_patient_id;
    INSERT INTO appointments (patient_id, clinic_id, copay_amount, status, created_at)
    VALUES (p_patient_id, p_clinic_id, p_copay, 'WAITING', NOW());
END;
$$;
