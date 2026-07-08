from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.evidence import EvidenceFile
from app.services.evidence_service import (
    get_evidence_for_vendor,
    save_evidence_file,
)
from app.services.vendor_service import get_vendor_by_id

router = APIRouter(prefix="/api/v1/evidence", tags=["Evidence"])

ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
}


@router.post(
    "/{vendor_id}",
    response_model=EvidenceFile,
    status_code=status.HTTP_201_CREATED,
)
async def upload_evidence(
    vendor_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> EvidenceFile:
    vendor = get_vendor_by_id(db, vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf evidence files are allowed.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    return save_evidence_file(
        db=db,
        vendor_id=vendor_id,
        original_file_name=file.filename or "uploaded_evidence",
        content_type=file.content_type,
        file_bytes=file_bytes,
    )


@router.get(
    "/{vendor_id}",
    response_model=list[EvidenceFile],
)
def list_vendor_evidence(
    vendor_id: str,
    db: Session = Depends(get_db),
) -> list[EvidenceFile]:
    vendor = get_vendor_by_id(db, vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    return get_evidence_for_vendor(db, vendor_id)