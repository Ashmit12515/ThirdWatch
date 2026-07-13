import json
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import ExtractionModel
from app.models import AssessmentModel, VendorModel
from app.schemas.assessment import RiskAssessment
from app.schemas.vendor import Vendor


def calculate_vendor_risk(vendor: Vendor) -> tuple[int, str, list[str]]:
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

    return score, tier, reasons


def assessment_model_to_schema(
    assessment: AssessmentModel,
    vendor: Vendor,
) -> RiskAssessment:
    return RiskAssessment(
        assessment_id=assessment.assessment_id,
        vendor=vendor,
        risk_score=assessment.risk_score,
        risk_tier=assessment.risk_tier,
        reasons=json.loads(assessment.reasons_json),
        created_at=assessment.created_at,
        scoring_version=assessment.scoring_version,
    )


def create_risk_assessment(db: Session, vendor: Vendor) -> RiskAssessment:
    score, tier, reasons = calculate_vendor_risk(vendor)

    assessment_count = db.query(func.count(AssessmentModel.assessment_id)).scalar() or 0
    assessment = AssessmentModel(
        assessment_id=f"A-{assessment_count + 1:03d}",
        vendor_id=vendor.vendor_id,
        risk_score=score,
        risk_tier=tier,
        reasons_json=json.dumps(reasons),
        created_at=datetime.now(timezone.utc),
        scoring_version="v1.0",
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment_model_to_schema(assessment, vendor)


def get_all_assessments(db: Session) -> list[RiskAssessment]:
    assessments = (
        db.query(AssessmentModel)
        .order_by(AssessmentModel.created_at.desc())
        .all()
    )

    results: list[RiskAssessment] = []

    for assessment in assessments:
        vendor = db.get(VendorModel, assessment.vendor_id)

        if vendor:
            from app.services.vendor_service import vendor_model_to_schema

            results.append(
                assessment_model_to_schema(
                    assessment,
                    vendor_model_to_schema(vendor),
                )
            )

    return results


def get_assessment_by_vendor_id(
    db: Session,
    vendor_id: str,
) -> RiskAssessment | None:
    assessment = (
        db.query(AssessmentModel)
        .filter(AssessmentModel.vendor_id == vendor_id)
        .order_by(AssessmentModel.created_at.desc())
        .first()
    )

    if assessment is None:
        return None

    from app.services.vendor_service import vendor_model_to_schema

    vendor = db.get(VendorModel, assessment.vendor_id)

    if vendor is None:
        return None

    return assessment_model_to_schema(
        assessment,
        vendor_model_to_schema(vendor),
    )
def recalculate_assessment_from_evidence(
    db: Session,
    vendor_id: str,
) -> RiskAssessment | None:
    from app.services.vendor_service import get_vendor_by_id

    vendor = get_vendor_by_id(db, vendor_id)

    if vendor is None:
        return None

    latest_extractions = (
        db.query(ExtractionModel)
        .filter(ExtractionModel.vendor_id == vendor_id)
        .order_by(ExtractionModel.extracted_at.desc())
        .all()
    )

    verified_controls: set[str] = set()

    for extraction in latest_extractions:
        findings = json.loads(extraction.findings_json)

        for finding in findings:
            if finding.get("status") == "Detected":
                verified_controls.add(finding.get("control", ""))

    adjusted_vendor = vendor.model_copy(
        update={
            "has_soc2": vendor.has_soc2 or "SOC 2" in verified_controls,
            "has_iso27001": vendor.has_iso27001
            or "ISO 27001" in verified_controls,
            "mfa_enabled": vendor.mfa_enabled or "MFA" in verified_controls,
            "encryption_at_rest": vendor.encryption_at_rest
            or "Encryption at Rest" in verified_controls,
            "incident_response_plan": vendor.incident_response_plan
            or "Incident Response Plan" in verified_controls,
        }
    )

    score, tier, reasons = calculate_vendor_risk(adjusted_vendor)

    assessment_count = (
        db.query(func.count(AssessmentModel.assessment_id)).scalar() or 0
    )

    assessment = AssessmentModel(
        assessment_id=f"A-{assessment_count + 1:03d}",
        vendor_id=vendor.vendor_id,
        risk_score=score,
        risk_tier=tier,
        reasons_json=json.dumps(reasons),
        created_at=datetime.now(timezone.utc),
        scoring_version="v1.1-evidence",
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment_model_to_schema(assessment, adjusted_vendor)
def get_assessment_history_by_vendor_id(
    db: Session,
    vendor_id: str,
) -> list[RiskAssessment]:
    assessments = (
        db.query(AssessmentModel)
        .filter(AssessmentModel.vendor_id == vendor_id)
        .order_by(AssessmentModel.created_at.desc())
        .all()
    )

    if not assessments:
        return []

    from app.services.vendor_service import vendor_model_to_schema

    vendor_model = db.get(VendorModel, vendor_id)

    if vendor_model is None:
        return []

    vendor = vendor_model_to_schema(vendor_model)

    return [
        assessment_model_to_schema(assessment, vendor)
        for assessment in assessments
    ]