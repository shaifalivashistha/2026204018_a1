db = db.getSiblingDB("careconnect");

// Workflow 3: Nearest Active Mobile Nurse within 5km
const result = db.NursePings.aggregate([
  {
    $geoNear: {
      near: { type: "Point", coordinates: [-73.985130, 40.748817] },
      distanceField: "dist.calculated",
      maxDistance: 50000000,
      query: { is_active: true },
      spherical: true
    }
  },
  { $limit: 1 }
]).toArray();

printjson(result);