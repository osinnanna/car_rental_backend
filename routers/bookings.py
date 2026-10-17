import math
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from models.car import Car
from models.booking import Booking
from schemas.booking import BookingCreate, BookingStatusUpdate, BookingResponse
from core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new car booking reservation."""
    car = db.query(Car).filter(Car.id == booking_in.car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    if not car.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This car is currently marked as unavailable for rental",
        )

    if booking_in.to_date < booking_in.from_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Return date cannot be earlier than rental start date",
        )

    # Calculate rental duration in days (minimum 1 day)
    delta_seconds = (booking_in.to_date - booking_in.from_date).total_seconds()
    rental_days = max(1, math.ceil(delta_seconds / 86400))
    total_cost = rental_days * car.price_per_day

    booking = Booking(
        user_id=current_user.id,
        car_id=car.id,
        from_date=booking_in.from_date,
        to_date=booking_in.to_date,
        message=booking_in.message,
        total_cost=total_cost,
        status="Pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/my-history")
def get_user_booking_history(
    status_filter: Optional[str] = Query(None, description="Filter by status: All, Pending, Returned, Confirmed, Cancelled"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve personal booking history with metrics matching the UI History Page."""
    base_query = db.query(Booking).filter(Booking.user_id == current_user.id)

    total_rented = base_query.count()
    returned_count = base_query.filter(Booking.status.ilike("Returned")).count()
    yet_to_return = base_query.filter(Booking.status.in_(["Confirmed", "Active"])).count()
    pending_count = base_query.filter(Booking.status.ilike("Pending")).count()

    filtered_query = base_query
    if status_filter and status_filter.lower() != "all":
        filtered_query = filtered_query.filter(Booking.status.ilike(status_filter))

    bookings = filtered_query.order_by(Booking.created_at.desc()).all()

    return {
        "metrics": {
            "total_rented": total_rented,
            "yet_to_return": yet_to_return,
            "returned": returned_count,
            "pending": pending_count,
        },
        "bookings": [BookingResponse.model_validate(b) for b in bookings],
    }


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve details of a specific booking."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if not current_user.is_admin and booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return booking


@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel a booking reservation."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if not current_user.is_admin and booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if booking.status in ["Cancelled", "Returned"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel a booking that is already {booking.status}",
        )

    booking.status = "Cancelled"
    db.commit()
    db.refresh(booking)
    return booking


# --- ADMIN BOOKING ENDPOINTS ---

@router.get("/admin/all", response_model=List[BookingResponse])
def get_all_bookings_admin(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Retrieve all bookings across all users."""
    query = db.query(Booking)
    if status_filter:
        query = query.filter(Booking.status.ilike(status_filter))
    return query.order_by(Booking.created_at.desc()).all()


@router.put("/admin/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(
    booking_id: int,
    status_update: BookingStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update booking status (Pending, Confirmed, Cancelled, Returned)."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    booking.status = status_update.status
    db.commit()
    db.refresh(booking)
    return booking
