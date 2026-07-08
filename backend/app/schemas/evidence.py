from datetime import datetime
from pydantic import BaseModel


class EvidenceFile(BaseModel):
    evidence_id: str
    vendor_id: str
    file_name: str
    content_type: str | None
    file_path: str
    uploaded_at: datetime