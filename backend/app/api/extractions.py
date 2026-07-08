from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.extraction import EvidenceExtraction
from app.services.evidence_extraction_service import extract_control_findings

router = APIRouter(prefix="/api/v1/extractions", tags=["Evidence Extraction"])


@router.get(
    "/{evidence_id}",
    response_model=EvidenceExtraction,
)
def get_evidence_extraction(
    evidence_id: str,
    db: Session = Depends(get_db),
) -> EvidenceExtraction:
    extraction = extract_control_findings(db, evidence_id)

    if extraction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evidence file '{evidence_id}' was not found.",
        )

    return extraction