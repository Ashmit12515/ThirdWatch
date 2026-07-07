from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import VendorModel
from app.schemas.vendor import Vendor, VendorCreate


def vendor_model_to_schema(vendor: VendorModel) -> Vendor:
    return Vendor(
        vendor_id=vendor.vendor_id,
        vendor_name=vendor.vendor_name,
        industry=vendor.industry,
        data_type=vendor.data_type,
        hosts_pii=vendor.hosts_pii,
        has_soc2=vendor.has_soc2,
        has_iso27001=vendor.has_iso27001,
        mfa_enabled=vendor.mfa_enabled,
        encryption_at_rest=vendor.encryption_at_rest,
        incident_response_plan=vendor.incident_response_plan,
        subprocessors_count=vendor.subprocessors_count,
        criticality=vendor.criticality,
        expected_risk_tier=vendor.expected_risk_tier,
    )


def get_all_vendors(db: Session) -> list[Vendor]:
    vendors = db.query(VendorModel).order_by(VendorModel.vendor_id).all()
    return [vendor_model_to_schema(vendor) for vendor in vendors]


def get_vendor_by_id(db: Session, vendor_id: str) -> Vendor | None:
    vendor = db.get(VendorModel, vendor_id)
    return vendor_model_to_schema(vendor) if vendor else None


def create_vendor(db: Session, vendor_data: VendorCreate) -> Vendor:
    vendor_count = db.query(func.count(VendorModel.vendor_id)).scalar() or 0
    vendor_id = f"V-{vendor_count + 1:03d}"

    vendor = VendorModel(
        vendor_id=vendor_id,
        vendor_name=vendor_data.vendor_name,
        industry=vendor_data.industry,
        data_type=vendor_data.data_type,
        hosts_pii=vendor_data.hosts_pii,
        has_soc2=vendor_data.has_soc2,
        has_iso27001=vendor_data.has_iso27001,
        mfa_enabled=vendor_data.mfa_enabled,
        encryption_at_rest=vendor_data.encryption_at_rest,
        incident_response_plan=vendor_data.incident_response_plan,
        subprocessors_count=vendor_data.subprocessors_count,
        criticality=vendor_data.criticality,
        expected_risk_tier="Pending assessment",
    )

    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    return vendor_model_to_schema(vendor)