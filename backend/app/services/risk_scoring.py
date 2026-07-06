from app.schemas.assessment import RiskAssessment
from app.schemas.vendor import Vendor


def assess_vendor_risk(vendor: Vendor) -> RiskAssessment:
    score = 0
    reasons: list[str] = []

    if vendor.hosts_pii:
        score += 20
        reasons.append("Vendor processes personally identifiable information.")

    if not vendor.has_soc2:
        score += 15
        reasons.append("SOC 2 certification is not available.")

    if not vendor.has_iso27001:
        score += 15
        reasons.append("ISO 27001 certification is not available.")

    if not vendor.mfa_enabled:
        score += 15
        reasons.append("Multi-factor authentication is not enabled.")

    if not vendor.encryption_at_rest:
        score += 15
        reasons.append("Encryption at rest is not enabled.")

    if not vendor.incident_response_plan:
        score += 10
        reasons.append("Incident response plan is not available.")

    if vendor.subprocessors_count >= 5:
        score += 5
        reasons.append(
            f"Vendor uses {vendor.subprocessors_count} subprocessors, increasing third-party exposure."
        )

    if vendor.criticality.lower() == "high":
        score += 15
        reasons.append("Vendor is classified as high criticality.")
    elif vendor.criticality.lower() == "medium":
        score += 8
        reasons.append("Vendor is classified as medium criticality.")

    if score >= 55:
        tier = "Tier 1"
    elif score >= 30:
        tier = "Tier 2"
    else:
        tier = "Tier 3"

    return RiskAssessment(
        vendor=vendor,
        risk_score=score,
        risk_tier=tier,
        reasons=reasons,
    )