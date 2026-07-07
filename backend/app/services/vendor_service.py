from app.schemas.vendor import Vendor, VendorCreate

VENDORS: list[Vendor] = [
    Vendor(
        vendor_id="V-001",
        vendor_name="CloudLedger Solutions",
        industry="FinTech",
        data_type="Financial and personal data",
        hosts_pii=True,
        has_soc2=True,
        has_iso27001=True,
        mfa_enabled=True,
        encryption_at_rest=True,
        incident_response_plan=True,
        subprocessors_count=3,
        criticality="High",
        expected_risk_tier="Tier 1",
    ),
    Vendor(
        vendor_id="V-002",
        vendor_name="QuickSurvey Labs",
        industry="Market Research",
        data_type="Customer survey data",
        hosts_pii=True,
        has_soc2=False,
        has_iso27001=False,
        mfa_enabled=True,
        encryption_at_rest=True,
        incident_response_plan=False,
        subprocessors_count=7,
        criticality="Medium",
        expected_risk_tier="Tier 2",
    ),
    Vendor(
        vendor_id="V-003",
        vendor_name="OfficeFlow Tools",
        industry="Productivity SaaS",
        data_type="Non-sensitive operational data",
        hosts_pii=False,
        has_soc2=False,
        has_iso27001=False,
        mfa_enabled=False,
        encryption_at_rest=False,
        incident_response_plan=False,
        subprocessors_count=1,
        criticality="Low",
        expected_risk_tier="Tier 3",
    ),
]

def create_vendor(vendor_data: VendorCreate) -> Vendor:
    next_vendor_number = len(VENDORS) + 1
    vendor_id = f"V-{next_vendor_number:03d}"

    vendor = Vendor(
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

    VENDORS.append(vendor)
    return vendor

def get_all_vendors() -> list[Vendor]:
    return VENDORS


def get_vendor_by_id(vendor_id: str) -> Vendor | None:
    return next((vendor for vendor in VENDORS if vendor.vendor_id == vendor_id), None)