from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.vendors import router as vendors_router
from app.api.assessments import router as assessments_router
from app.database import Base, engine
from app.api import evidence
from app.api import extractions
from app import models

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Vendor Risk Governance API",
    version="0.1.0",
    description="An explainable vendor-risk assessment platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors_router)
app.include_router(assessments_router)
app.include_router(evidence.router)
app.include_router(extractions.router)

@app.get("/")
def root():
    return {
        "message": "Vendor Risk Governance API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "vendor-risk-governance-api",
    }