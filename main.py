import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from database import db, create_document, get_documents
from schemas import Complaint as ComplaintModel, Panchayat as PanchayatModel, Funds as FundsModel

app = FastAPI(title="Ruralytics JSON-like API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "Ruralytics API", "status": "ok"}

# Helper to convert Mongo documents

def _serialize(doc):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return d

# Panchayats endpoints (JSON Server-style)
@app.get("/panchayats")
def list_panchayats():
    items = get_documents("panchayat")
    data = [_serialize(x) for x in items]
    if not data:
        data = [
            {"panchayat_id":"PNC001","name":"Arjunpur","district":"Solan","state":"Himachal Pradesh"},
            {"panchayat_id":"PNC002","name":"Bhavani","district":"Krishnagiri","state":"Tamil Nadu"},
            {"panchayat_id":"PNC003","name":"Chandigarh Rural","district":"Chandigarh","state":"Chandigarh"}
        ]
    return data

@app.post("/panchayats")
def create_panchayat(payload: PanchayatModel):
    inserted_id = create_document("panchayat", payload)
    return {"id": inserted_id, **payload.model_dump()}

# Complaints endpoints (GET + POST)
@app.get("/complaints")
def list_complaints():
    items = get_documents("complaint")
    return [_serialize(x) for x in items]

@app.post("/complaints")
def create_complaint(payload: ComplaintModel):
    if not payload.name or not payload.description:
        raise HTTPException(status_code=400, detail="Name and description are required")
    inserted_id = create_document("complaint", payload)
    return {"id": inserted_id, **payload.model_dump()}

# Funds endpoints
@app.get("/funds")
def list_funds():
    items = get_documents("funds")
    data = [_serialize(x) for x in items]
    if not data:
        data = [
            {"panchayat_id":"PNC001","year":2024,"allocated":120,"utilized":95,"pending":25},
            {"panchayat_id":"PNC001","year":2023,"allocated":110,"utilized":90,"pending":20},
            {"panchayat_id":"PNC002","year":2024,"allocated":130,"utilized":100,"pending":30},
            {"panchayat_id":"PNC003","year":2024,"allocated":100,"utilized":70,"pending":30}
        ]
    return data

@app.post("/funds")
def create_funds(payload: FundsModel):
    inserted_id = create_document("funds", payload)
    return {"id": inserted_id, **payload.model_dump()}

# Analysis endpoint (AI-style mock recommendations)
@app.get("/analysis")
def list_analysis(panchayat_id: Optional[str] = None):
    filter_dict = {"panchayat_id": panchayat_id} if panchayat_id else {}
    items = get_documents("analysis", filter_dict)
    if not items:
        defaults = [
            {
                "title": "Boost School Attendance",
                "points": ["Introduce weekly attendance dashboards", "Provide bicycle support for long-distance students"],
                "sdg_tag": "SDG4",
            },
            {
                "title": "Strengthen Primary Healthcare",
                "points": ["Mobile immunization clinics every Friday", "Digitize maternal health tracking"],
                "sdg_tag": "SDG3",
            },
            {
                "title": "Optimize Water Usage",
                "points": ["Repair minor leakage points within 7 days", "Adopt micro-irrigation for 30% farms"],
                "sdg_tag": "SDG6",
            },
        ]
        return defaults
    return [_serialize(x) for x in items]

# Health check
@app.get("/test")
def test_services():
    try:
        collections = db.list_collection_names() if db else []
        return {"backend": "running", "db": bool(db), "collections": collections[:10]}
    except Exception as e:
        return {"backend": "running", "db": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
