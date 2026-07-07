from datetime import datetime
from pydantic import BaseModel

from app.schemas.vendor import Vendor


class RiskAssessment(BaseModel):
    assessment_id: str
    vendor: Vendor
    risk_score: int
    risk_tier: str
    reasons: list[str]
    created_at: datetime
    scoring_version: str = "v1.0"