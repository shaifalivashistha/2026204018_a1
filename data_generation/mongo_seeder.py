import random
import os
from datetime import datetime, timezone
from pymongo import MongoClient

def seed():
    client = MongoClient(os.getenv("CARECONNECT_MONGO_URI", "mongodb://localhost:27017/"))
    db = client[os.getenv("CARECONNECT_MONGO_DB", "careconnect")]

    # 1. Seed 500,000 Geospatial Telemetry Pings
    print("Seeding NursePings (500,000 pings)...")
    pings = []
    batch_size = 50000
    
    for i in range(500000):
        ping = {
            "nurse_id": random.randint(1, 500),
            "is_active": random.choice([True, False]),
            "location": {
                "type": "Point",
                "coordinates": [
                    -73.985130 + (random.uniform(-0.1, 0.1)),
                    40.748817 + (random.uniform(-0.1, 0.1))
                ]
            },
            "created_at": datetime.now(timezone.utc)
        }
        pings.append(ping)
        
        if len(pings) == batch_size:
            db.NursePings.insert_many(pings)
            pings = []
            print(f"Inserted {i + 1} pings...")

    # 2. Seed Patient Reviews
    print("Seeding PatientReviews...")
    tags = ["Friendly", "Punctual", "Attentive", "Rushed", "Professional", "Empathetic"]
    reviews = []
    for _ in range(5000):
        reviews.append({
            "patient_id": random.randint(1, 1000),
            "rating": random.randint(1, 5),
            "bedside_manner_tags": random.sample(tags, k=random.randint(1, 3)),
            "created_at": datetime.now(timezone.utc)
        })
    db.PatientReviews.insert_many(reviews)
    print("MongoDB Data Generation Complete!")

if __name__ == "__main__":
    seed()
