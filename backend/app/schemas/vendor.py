from pydantic import BaseModel, Field


class Vendor(BaseModel):
    vendor_id: str
    vendor_name: str
    industry: str
    data_type: str
    hosts_pii: bool
    has_soc2: bool
    has_iso27001: bool
    mfa_enabled: bool
    encryption_at_rest: bool
    incident_response_plan: bool
    subprocessors_count: int = Field(ge=0)
    criticality: str
    expected_risk_tier: str