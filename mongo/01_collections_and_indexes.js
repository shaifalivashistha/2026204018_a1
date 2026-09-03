db = db.getSiblingDB("careconnect");

// 2dsphere index on NursePings location
db.NursePings.createIndex({ location: "2dsphere" });

// 2-hour TTL index on created_at
db.NursePings.createIndex({ created_at: 1 }, { expireAfterSeconds: 7200 });
