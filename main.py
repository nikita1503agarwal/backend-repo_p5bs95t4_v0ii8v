from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
from database import db, create_document, get_documents
from schemas import Contact
import os

app = FastAPI(title="Focus Security API")

# CORS setup - allow the frontend origin
frontend_url = os.getenv("FRONTEND_URL")
origins = [frontend_url] if frontend_url else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Focus Security API running"}

@app.get("/test")
async def test_connection():
    try:
        # Check DB availability and list collections
        collections = []
        if db is not None:
            collections = db.list_collection_names()
        return {
            "backend": "ok",
            "database": "ok" if db is not None else "not-configured",
            "database_url": bool(os.getenv("DATABASE_URL")),
            "database_name": os.getenv("DATABASE_NAME"),
            "connection_status": "connected" if db is not None else "n/a",
            "collections": collections,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
async def create_contact(payload: Contact):
    try:
        contact_id = create_document("contact", payload)
        return {"status": "ok", "id": contact_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
