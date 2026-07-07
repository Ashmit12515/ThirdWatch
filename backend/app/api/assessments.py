from fastapi import APIRouter, HTTPException, status

from app.schemas.assessment import RiskAssessment
from app.schemas.vendor import VendorCreate
from app.services.risk_scoring import (
    create_risk_assessment,
    get_all_assessments,
    get_assessment_by_vendor_id,
)
from app.services.vendor_service import create_vendor, get_vendor_by_id

router = APIRouter(prefix="/api/v1/assessments", tags=["Assessments"])


@router.post(
    "/",
    response_model=RiskAssessment,
    status_code=status.HTTP_201_CREATED,
)
def create_vendor_assessment(vendor_data: VendorCreate) -> RiskAssessment:
    vendor = create_vendor(vendor_data)
    return create_risk_assessment(vendor)


@router.get("/", response_model=list[RiskAssessment])
def list_assessments() -> list[RiskAssessment]:
    return get_all_assessments()


@router.get("/{vendor_id}", response_model=RiskAssessment)
def get_vendor_assessment(vendor_id: str) -> RiskAssessment:
    vendor = get_vendor_by_id(vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    assessment = get_assessment_by_vendor_id(vendor_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail=f"No assessment exists yet for vendor '{vendor_id}'.",
        )

    return assessment