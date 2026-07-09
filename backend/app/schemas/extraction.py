from datetime import datetime

from pydantic import BaseModel


class ControlFinding(BaseModel):
    control: str
    status: str
    evidence_text: str


class EvidenceExtraction(BaseModel):
    evidence_id: str
    vendor_id: str
    findings: list[ControlFinding]
    extraction_method: str
    extracted_at: datetime