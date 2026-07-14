import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import EvidenceModel, ExtractionModel
from app.schemas.extraction import ControlFinding, EvidenceExtraction
from app.ai.control_extraction import extract_controls


LEGACY_CONTROL_RULES = {
    "SOC 2": ["soc 2", "soc2", "soc 2 type ii", "soc 2 type 2"],
    "ISO 27001": ["iso 27001", "iso27001"],
    "MFA": ["mfa", "multi-factor authentication", "multifactor authentication"],
    "Encryption at Rest": [
        "encryption at rest",
        "encrypted at rest",
        "aes-256",
        "aes 256",
    ],
    "Incident Response Plan": [
        "incident response plan",
        "incident response",
        "ir plan",
    ],
}


def legacy_find_matching_line(text: str, keywords: list[str]) -> str | None:
    for line in text.splitlines():
        normalized_line = line.strip().lower()

        if any(keyword in normalized_line for keyword in keywords):
            return line.strip()

    return None


def extraction_model_to_schema(
    extraction: ExtractionModel,
) -> EvidenceExtraction:
    findings_data = json.loads(extraction.findings_json)

    return EvidenceExtraction(
        evidence_id=extraction.evidence_id,
        vendor_id=extraction.vendor_id,
        findings=[ControlFinding(**finding) for finding in findings_data],
        extraction_method=extraction.extraction_method,
        extracted_at=extraction.extracted_at,
    )


def get_existing_extraction(
    db: Session,
    evidence_id: str,
) -> EvidenceExtraction | None:
    extraction = (
        db.query(ExtractionModel)
        .filter(ExtractionModel.evidence_id == evidence_id)
        .order_by(ExtractionModel.extracted_at.desc())
        .first()
    )

    if extraction is None:
        return None

    return extraction_model_to_schema(extraction)


def extract_control_findings(
    db: Session,
    evidence_id: str,
) -> EvidenceExtraction | None:
    existing_extraction = get_existing_extraction(db, evidence_id)

    if existing_extraction is not None:
        return existing_extraction

    evidence = db.get(EvidenceModel, evidence_id)

    if evidence is None:
        return None

    findings: list[ControlFinding] = []

    if evidence.content_type == "text/plain":
        file_path = Path(evidence.file_path)

        if not file_path.exists():
            return None

        text = file_path.read_text(encoding="utf-8", errors="ignore")
        print("=" * 60)
        print("LLM EXTRACTION STARTED")
        print("=" * 60)
        llm_result=extract_controls(text)
        print(llm_result)
        print("=" * 60)
        print("LLM EXTRACTION FINISHED")
        print("=" * 60)
        for finding in llm_result.findings:
            findings.append(
                ControlFinding(
                    control=finding.control.value,
                    status="Detected" if finding.implemented else "Not Detected",
                    evidence_text=finding.evidence

                )
            )

    extraction_count = (
        db.query(func.count(ExtractionModel.extraction_id)).scalar() or 0
    )

    extraction = ExtractionModel(
        extraction_id=f"X-{extraction_count + 1:03d}",
        evidence_id=evidence.evidence_id,
        vendor_id=evidence.vendor_id,
        findings_json=json.dumps(
            [finding.model_dump() for finding in findings],
        ),
        extraction_method="llm_v1",
        extracted_at=datetime.now(timezone.utc),
    )

    db.add(extraction)
    db.commit()
    db.refresh(extraction)

    return extraction_model_to_schema(extraction)