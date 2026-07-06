from fastapi import FastAPI

from app.api.vendors import router as vendors_router
from app.api.assessments import router as assessments_router

app = FastAPI(
    title="Vendor Risk Governance API",
    version="0.1.0",
    description="An explainable vendor-risk assessment platform.",
)

app.include_router(vendors_router)
app.include_router(assessments_router)


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