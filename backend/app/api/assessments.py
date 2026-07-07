from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
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
def create_vendor_assessment(
    vendor_data: VendorCreate,
    db: Session = Depends(get_db),
) -> RiskAssessment:
    vendor = create_vendor(db, vendor_data)
    return create_risk_assessment(db, vendor)


@router.get("/", response_model=list[RiskAssessment])
def list_assessments(
    db: Session = Depends(get_db),
) -> list[RiskAssessment]:
    return get_all_assessments(db)


@router.get("/{vendor_id}", response_model=RiskAssessment)
def get_vendor_assessment(
    vendor_id: str,
    db: Session = Depends(get_db),
) -> RiskAssessment:
    vendor = get_vendor_by_id(db, vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    assessment = get_assessment_by_vendor_id(db, vendor_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail=f"No assessment exists yet for vendor '{vendor_id}'.",
        )

    return assessment