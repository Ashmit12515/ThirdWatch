from app.schemas.vendor import Vendor


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


def get_all_vendors() -> list[Vendor]:
    return VENDORS


def get_vendor_by_id(vendor_id: str) -> Vendor | None:
    return next((vendor for vendor in VENDORS if vendor.vendor_id == vendor_id), None)