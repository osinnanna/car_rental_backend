from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.car import Car
from schemas.car import CarCreate, CarUpdate, CarResponse
from core.deps import get_current_admin

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("", response_model=List[CarResponse])
def get_cars(
    category_id: Optional[int] = Query(None, description="Filter by category"),
    brand_id: Optional[int] = Query(None, description="Filter by brand"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type"),
    transmission: Optional[str] = Query(None, description="Filter by transmission (Automatic/Manual)"),
    is_featured: Optional[bool] = Query(None, description="Filter featured cars"),
    is_slider: Optional[bool] = Query(None, description="Filter slider cars"),
    min_price: Optional[float] = Query(None, description="Minimum price per day"),
    max_price: Optional[float] = Query(None, description="Maximum price per day"),
    search: Optional[str] = Query(None, description="Search keyword in title or overview"),
    available_only: bool = Query(True, description="Only return available cars"),
    db: Session = Depends(get_db),
):
    """Search and filter rental fleet vehicles."""
    query = db.query(Car)

    if available_only:
        query = query.filter(Car.is_available.is_(True))
    if category_id is not None:
        query = query.filter(Car.category_id == category_id)
    if brand_id is not None:
        query = query.filter(Car.brand_id == brand_id)
    if fuel_type:
        query = query.filter(Car.fuel_type.ilike(fuel_type))
    if transmission:
        query = query.filter(Car.transmission.ilike(transmission))
    if is_featured is not None:
        query = query.filter(Car.is_featured == is_featured)
    if is_slider is not None:
        query = query.filter(Car.is_slider == is_slider)
    if min_price is not None:
        query = query.filter(Car.price_per_day >= min_price)
    if max_price is not None:
        query = query.filter(Car.price_per_day <= max_price)
    if search:
        search_filter = f"%{search}%"
        query = query.filter((Car.title.ilike(search_filter)) | (Car.overview.ilike(search_filter)))

    return query.order_by(Car.created_at.desc()).all()


@router.get("/featured", response_model=List[CarResponse])
def get_featured_cars(db: Session = Depends(get_db)):
    """Retrieve featured cars for the homepage 'Featured Cars' section."""
    return db.query(Car).filter(Car.is_featured.is_(True), Car.is_available.is_(True)).all()


@router.get("/slider", response_model=List[CarResponse])
def get_slider_cars(db: Session = Depends(get_db)):
    """Retrieve top cars for the Hero banner slideshow."""
    return db.query(Car).filter(Car.is_slider.is_(True), Car.is_available.is_(True)).all()


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    """Retrieve full details of a specific car."""
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car


@router.post("", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    car_in: CarCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Add a new vehicle to the rental fleet."""
    car = Car(**car_in.model_dump())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    car_id: int,
    car_in: CarUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update specifications, pricing, features, or availability of a car."""
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    update_data = car_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Remove a car from the fleet."""
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    db.delete(car)
    db.commit()
    return None
