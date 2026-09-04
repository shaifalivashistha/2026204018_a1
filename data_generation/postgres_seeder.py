import psycopg2
import random
import os
from datetime import datetime, timedelta

CONN_PARAMS = {
    "dbname": os.getenv("CARECONNECT_DB_NAME", "careconnect"),
    "user": os.getenv("CARECONNECT_DB_USER", "postgres"),
    "password": os.getenv("CARECONNECT_DB_PASSWORD"),
    "host": os.getenv("CARECONNECT_DB_HOST", "localhost"),
    "port": os.getenv("CARECONNECT_DB_PORT", "5432")
}

def seed():
    conn = psycopg2.connect(**CONN_PARAMS)
    cur = conn.cursor()
    
    print("Clearing old data...")
    cur.execute("TRUNCATE TABLE appointments, wallet_audit_logs, patients, clinics RESTART IDENTITY CASCADE;")
    conn.commit()

    print("Seeding Patients...")
    patients_data = [(f"Patient_{i}", random.uniform(100.0, 5000.0)) for i in range(1000)]
    cur.executemany("INSERT INTO patients (name, hsa_balance) VALUES (%s, %s)", patients_data)
    
    print("Seeding Clinics...")
    clinics_data = [(f"Clinic_{i}", 40.7 + random.random(), -73.9 + random.random(), True) for i in range(50)]
    cur.executemany("INSERT INTO clinics (name, latitude, longitude, is_accepting_patients) VALUES (%s, %s, %s, %s)", clinics_data)
    conn.commit()

    print("Seeding Appointments (50,000)...")
    start_date = datetime.now() - timedelta(days=60)
    appointments = []
    for _ in range(50000):
        p_id = random.randint(1, 1000)
        c_id = random.randint(1, 50)
        copay = round(random.uniform(10.0, 150.0), 2)
        created_at = start_date + timedelta(minutes=random.randint(0, 86400))
        appointments.append((p_id, c_id, copay, 'DISCHARGED', created_at))
    
    cur.executemany("""
        INSERT INTO appointments (patient_id, clinic_id, copay_amount, status, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, appointments)
    
    print("Generating Ledger/Audit Logs (100,000 updates)...")
    for _ in range(100000):
        p_id = random.randint(1, 1000)
        amt = round(random.uniform(5.0, 50.0), 2)
        cur.execute("UPDATE patients SET hsa_balance = hsa_balance + %s WHERE id = %s", (amt, p_id))

    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL Data Generation Complete!")

if __name__ == "__main__":
    seed()
