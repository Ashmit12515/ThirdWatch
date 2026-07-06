from fastapi import APIRouter, HTTPException

from app.schemas.vendor import Vendor
from app.services.vendor_service import get_all_vendors, get_vendor_by_id

router = APIRouter(prefix="/api/v1/vendors", tags=["Vendors"])


@router.get("/", response_model=list[Vendor])
def list_vendors() -> list[Vendor]:
    return get_all_vendors()


@router.get("/{vendor_id}", response_model=Vendor)
def get_vendor(vendor_id: str) -> Vendor:
    vendor = get_vendor_by_id(vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    return vendor