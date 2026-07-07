from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vendor import Vendor
from app.services.vendor_service import get_all_vendors, get_vendor_by_id

router = APIRouter(prefix="/api/v1/vendors", tags=["Vendors"])


@router.get("/", response_model=list[Vendor])
def list_vendors(db: Session = Depends(get_db)) -> list[Vendor]:
    return get_all_vendors(db)


@router.get("/{vendor_id}", response_model=Vendor)
def get_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
) -> Vendor:
    vendor = get_vendor_by_id(db, vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor '{vendor_id}' was not found.",
        )

    return vendor