from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.car import Brand
from schemas.car import BrandCreate, BrandUpdate, BrandResponse
from core.deps import get_current_admin

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    """Retrieve all vehicle brands (for 'Top Brands' section and car filters)."""
    return db.query(Brand).order_by(Brand.name.asc()).all()


@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a single brand."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand


@router.post("", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
def create_brand(
    brand_in: BrandCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Create a new vehicle brand."""
    existing = db.query(Brand).filter(Brand.name == brand_in.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Brand name already exists")

    brand = Brand(name=brand_in.name, logo_url=brand_in.logo_url)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update an existing brand name or logo."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    if brand_in.name is not None:
        brand.name = brand_in.name
    if brand_in.logo_url is not None:
        brand.logo_url = brand_in.logo_url

    db.commit()
    db.refresh(brand)
    return brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Delete a vehicle brand."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    db.delete(brand)
    db.commit()
    return None
