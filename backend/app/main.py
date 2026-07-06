from fastapi import FastAPI

app = FastAPI(
    title="Vendor Risk Governance API",
    version="0.1.0",
    description="An explainable vendor-risk assessment platform."
)

@app.get("/")
def root():
    return {
        "message": "Vendor Risk Governance API is running",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "vendor-risk-governance-api"
    }