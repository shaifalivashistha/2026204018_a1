CREATE OR REPLACE FUNCTION log_hsa_balance_change()
RETURNS TRIGGER AS $$
DECLARE
    diff DECIMAL(10,2);
    action_str VARCHAR(20);
BEGIN
    IF OLD.hsa_balance IS DISTINCT FROM NEW.hsa_balance THEN
        diff := NEW.hsa_balance - OLD.hsa_balance;
        IF diff > 0 THEN action_str := 'CREDIT'; ELSE action_str := 'DEBIT'; END IF;
        INSERT INTO wallet_audit_logs (patient_id, amount_changed, action_type, balance_after, timestamp)
        VALUES (NEW.id, ABS(diff), action_str, NEW.hsa_balance, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hsa_balance_audit
AFTER UPDATE OF hsa_balance ON patients
FOR EACH ROW
WHEN (OLD.hsa_balance IS DISTINCT FROM NEW.hsa_balance)
EXECUTE FUNCTION log_hsa_balance_change();
