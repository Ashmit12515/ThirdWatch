from pydantic import BaseModel
from app.ai.enums import ControlName


class ControlFinding(BaseModel):
    control: ControlName
    implemented: bool
    evidence: str


class ControlExtraction(BaseModel):
    findings: list[ControlFinding]