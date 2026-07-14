from enum import Enum


class ControlName(str, Enum):
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    MFA = "MFA"
    ENCRYPTION_AT_REST = "ENCRYPTION_AT_REST"
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"