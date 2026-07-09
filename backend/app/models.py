from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VendorModel(Base):
    __tablename__ = "vendors"

    vendor_id: Mapped[str] = mapped_column(String, primary_key=True)
    vendor_name: Mapped[str] = mapped_column(String, nullable=False)
    industry: Mapped[str] = mapped_column(String, nullable=False)
    data_type: Mapped[str] = mapped_column(Text, nullable=False)

    hosts_pii: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_soc2: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_iso27001: Mapped[bool] = mapped_column(Boolean, nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    encryption_at_rest: Mapped[bool] = mapped_column(Boolean, nullable=False)
    incident_response_plan: Mapped[bool] = mapped_column(Boolean, nullable=False)

    subprocessors_count: Mapped[int] = mapped_column(Integer, nullable=False)
    criticality: Mapped[str] = mapped_column(String, nullable=False)
    expected_risk_tier: Mapped[str] = mapped_column(String, nullable=False)


class AssessmentModel(Base):
    __tablename__ = "assessments"

    assessment_id: Mapped[str] = mapped_column(String, primary_key=True)
    vendor_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_tier: Mapped[str] = mapped_column(String, nullable=False)
    reasons_json: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    scoring_version: Mapped[str] = mapped_column(
        String,
        default="v1.0",
        nullable=False,
    )

class EvidenceModel(Base):
    __tablename__ = "evidence_files"

    evidence_id: Mapped[str] = mapped_column(String, primary_key=True)
    vendor_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str | None] = mapped_column(String, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

class ExtractionModel(Base):
    __tablename__ = "extractions"

    extraction_id: Mapped[str] = mapped_column(String, primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    vendor_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    findings_json: Mapped[str] = mapped_column(Text, nullable=False)
    extraction_method: Mapped[str] = mapped_column(
        String,
        default="rule_based_v1",
        nullable=False,
    )
    extracted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )