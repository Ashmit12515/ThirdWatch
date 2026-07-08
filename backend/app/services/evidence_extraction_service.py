from pathlib import Path

from sqlalchemy.orm import Session

from app.models import EvidenceModel
from app.schemas.extraction import ControlFinding, EvidenceExtraction


CONTROL_RULES = {
    "SOC 2": [
        "soc 2",
        "soc2",
        "soc 2 type ii",
        "soc 2 type 2",
    ],
    "ISO 27001": [
        "iso 27001",
        "iso27001",
    ],
    "MFA": [
        "mfa",
        "multi-factor authentication",
        "multifactor authentication",
    ],
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


def find_matching_line(text: str, keywords: list[str]) -> str | None:
    for line in text.splitlines():
        normalized_line = line.strip().lower()

        if any(keyword in normalized_line for keyword in keywords):
            return line.strip()

    return None


def extract_control_findings(
    db: Session,
    evidence_id: str,
) -> EvidenceExtraction | None:
    evidence = db.get(EvidenceModel, evidence_id)

    if evidence is None:
        return None

    if evidence.content_type != "text/plain":
        return EvidenceExtraction(
            evidence_id=evidence.evidence_id,
            vendor_id=evidence.vendor_id,
            findings=[],
        )

    file_path = Path(evidence.file_path)

    if not file_path.exists():
        return None

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    findings: list[ControlFinding] = []

    for control, keywords in CONTROL_RULES.items():
        matching_line = find_matching_line(text, keywords)

        if matching_line:
            findings.append(
                ControlFinding(
                    control=control,
                    status="Detected",
                    evidence_text=matching_line,
                )
            )

    return EvidenceExtraction(
        evidence_id=evidence.evidence_id,
        vendor_id=evidence.vendor_id,
        findings=findings,
    )