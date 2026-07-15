from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.assessment import RiskAssessment
from app.schemas.vendor import VendorCreate
from app.services.risk_scoring import (
    create_risk_assessment,
    get_all_assessments,
    get_assessment_by_vendor_id,
)
from app.services.evidence_service import save_evidence_file
from app.services.vendor_service import create_vendor, get_vendor_by_id
from app.services.risk_scoring import (
    create_risk_assessment,
    get_all_assessments,
    get_assessment_by_vendor_id,
    get_assessment_history_by_vendor_id,
    recalculate_assessment_from_evidence,
)
router = APIRouter(prefix="/api/v1/assessments", tags=["Assessments"])


@router.post(
    "/",
    response_model=RiskAssessment,
    status_code=status.HTTP_201_CREATED,
)
async def create_vendor_assessment(
    vendor_data: str = Form(...),
    evidence_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
) -> RiskAssessment:

    vendor = VendorCreate.model_validate_json(vendor_data)

    created_vendor = create_vendor(
        db,
        vendor,
    )

    assessment = create_risk_assessment(
        db,
        created_vendor,
    )

    if evidence_file is not None:

        file_bytes = await evidence_file.read()

        save_evidence_file(
            db=db,
            vendor_id=created_vendor.vendor_id,
            original_file_name=evidence_file.filename,
            content_type=evidence_file.content_type,
            file_bytes=file_bytes,
        )

    return assessment


@router.get("/", response_model=list[RiskAssessment])
def list_assessments(
    db: Session = Depends(get_db),
) -> list[RiskAssessment]:
    return get_all_assessments(db)

@router.get("/{vendor_id}/history", response_model=list[RiskAssessment])
def get_assessment_history(
    vendor_id: str,
    db: Session = Depends(get_db),
) -> list[RiskAssessment]:
    return get_assessment_history_by_vendor_id(db, vendor_id)

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

@router.post("/{vendor_id}/recalculate", response_model=RiskAssessment)
def recalculate_assessment(
    vendor_id: str,
    db: Session = Depends(get_db),
) -> RiskAssessment:
    assessment = recalculate_assessment_from_evidence(db, vendor_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found.",
        )

    return assessment