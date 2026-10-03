from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Gaming YouTube Thumbnail Designer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str

class ThemeUpdate(BaseModel):
    theme_preference: str

# In-memory data
data_store = [
    {"id": 1, "title": "Epic Gaming Setup", "status": "active", "score": 9.5, "timestamp": "2023-10-27T10:00:00Z"},
    {"id": 2, "title": "Speedrun Tutorial", "status": "pending", "score": 8.2, "timestamp": "2023-10-27T11:30:00Z"}
]

user_settings = {"theme_preference": "dark"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_items": len(data_store), "average_score": sum(d['score'] for d in data_store) / len(data_store)}

@app.post("/api/reviews")
def submit_review(review: Review):
    data_store.append(review.dict())
    return {"message": "Review submitted successfully"}

@app.patch("/api/settings/theme")
def update_theme(settings: ThemeUpdate):
    if settings.theme_preference not in ["light", "dark"]:
        raise HTTPException(status_code=400, detail="Invalid theme")
    user_settings["theme_preference"] = settings.theme_preference
    return user_settings