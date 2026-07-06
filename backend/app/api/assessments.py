from fastapi import APIRouter, HTTPException

from app.schemas.assessment import RiskAssessment
from app.services.risk_scoring import assess_vendor_risk
from app.services.vendor_service import get_vendor_by_id

router = APIRouter(prefix="/api/v1/assessments", tags=["Assessments"])


@router.get("/{vendor_id}", response_model=RiskAssessment)
def get_vendor_assessment(vendor_id: str) -> RiskAssessment:
    vendor = get_vendor_by_id(vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    return assess_vendor_risk(vendor)