from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sys
import os
from fastapi.middleware.cors import CORSMiddleware

# Allow imports from backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from storage.activity_db import insert_log

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define structure of incoming activity log
class ActivityLog(BaseModel):
    url: str
    duration: int
    timestamp: str


# API endpoint to receive logs
@app.post("/log-activity")
def log_activity(logs: List[ActivityLog]):
    for log in logs:
        insert_log(log.url, log.duration, log.timestamp)

    return {
        "status": "success",
        "message": f"{len(logs)} logs inserted successfully"
    }
from storage.activity_db import get_all_logs

@app.get("/get-logs")
def get_logs():
    return get_all_logs()

@app.get("/")
def root():
    return {"message": "EmoTrace API is running"}
