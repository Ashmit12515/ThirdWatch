from pydantic import BaseModel

from app.schemas.vendor import Vendor


class RiskAssessment(BaseModel):
    vendor: Vendor
    risk_score: int
    risk_tier: str
    reasons: list[str]