from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import EvidenceModel
from app.schemas.evidence import EvidenceFile

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


def evidence_model_to_schema(evidence: EvidenceModel) -> EvidenceFile:
    return EvidenceFile(
        evidence_id=evidence.evidence_id,
        vendor_id=evidence.vendor_id,
        file_name=evidence.file_name,
        content_type=evidence.content_type,
        file_path=evidence.file_path,
        uploaded_at=evidence.uploaded_at,
    )


def save_evidence_file(
    db: Session,
    vendor_id: str,
    original_file_name: str,
    content_type: str | None,
    file_bytes: bytes,
) -> EvidenceFile:
    evidence_count = db.query(func.count(EvidenceModel.evidence_id)).scalar() or 0
    evidence_id = f"E-{evidence_count + 1:03d}"

    safe_file_name = f"{uuid4().hex}_{original_file_name}"
    file_path = UPLOADS_DIR / safe_file_name
    file_path.write_bytes(file_bytes)

    evidence = EvidenceModel(
        evidence_id=evidence_id,
        vendor_id=vendor_id,
        file_name=original_file_name,
        content_type=content_type,
        file_path=str(file_path),
        uploaded_at=datetime.now(timezone.utc),
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence_model_to_schema(evidence)


def get_evidence_for_vendor(
    db: Session,
    vendor_id: str,
) -> list[EvidenceFile]:
    evidence_files = (
        db.query(EvidenceModel)
        .filter(EvidenceModel.vendor_id == vendor_id)
        .order_by(EvidenceModel.uploaded_at.desc())
        .all()
    )

    return [evidence_model_to_schema(item) for item in evidence_files]