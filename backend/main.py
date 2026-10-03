from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Indoor Operations API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PickupRequest(BaseModel):
    id: int
    customer_name: str
    contact_phone: str
    pickup_address: str
    carpet_details: str
    status: str
    driver_id: Optional[int] = None
    timestamp: str

class Review(BaseModel):
    pickup_id: int
    score: int
    notes: str

pickups = [
    {"id": 1, "customer_name": "John Doe", "contact_phone": "555-0101", "pickup_address": "123 Maple St", "carpet_details": "Persian, 8x10", "status": "pending", "driver_id": None, "timestamp": "2023-10-27T10:00:00"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_pickups": len(pickups), "completion_rate": 0.0}

@app.get("/api/pickups", response_model=List[PickupRequest])
def get_pickups(status: Optional[str] = None):
    if status:
        return [p for p in pickups if p["status"] == status]
    return pickups

@app.post("/api/pickups")
def create_pickup(data: PickupRequest):
    pickups.append(data.dict())
    return data

@app.patch("/api/pickups/{pickup_id}/status")
def update_status(pickup_id: int, status: str, driver_id: Optional[int] = None):
    for p in pickups:
        if p["id"] == pickup_id:
            p["status"] = status
            if driver_id: p["driver_id"] = driver_id
            return p
    raise HTTPException(status_code=404, detail="Pickup not found")

@app.post("/api/reviews")
def submit_review(review: Review):
    return {"message": "Review recorded", "data": review}