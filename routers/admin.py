from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import get_db
from models.user import User
from models.car import Car, Brand
from models.booking import Booking
from models.contact import ContactQuery, Subscriber
from schemas.user import UserResponse
from core.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Operations"])


@router.get("/dashboard")
def get_admin_dashboard_metrics(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin Dashboard: Summary counts and metrics required by project specification."""
    total_users = db.query(User).filter(User.is_admin.is_(False)).count()
    total_cars = db.query(Car).count()
    total_brands = db.query(Brand).count()
    total_bookings = db.query(Booking).count()
    total_subscribers = db.query(Subscriber).count()
    total_queries = db.query(ContactQuery).count()

    # Total revenue from confirmed or returned rentals
    total_revenue = (
        db.query(func.sum(Booking.total_cost))
        .filter(Booking.status.in_(["Confirmed", "Returned"]))
        .scalar()
        or 0.0
    )

    # Bookings grouped by status
    pending_bookings = db.query(Booking).filter(Booking.status.ilike("Pending")).count()
    confirmed_bookings = db.query(Booking).filter(Booking.status.ilike("Confirmed")).count()
    returned_bookings = db.query(Booking).filter(Booking.status.ilike("Returned")).count()
    cancelled_bookings = db.query(Booking).filter(Booking.status.ilike("Cancelled")).count()

    return {
        "total_users": total_users,
        "total_cars": total_cars,
        "total_brands": total_brands,
        "total_bookings": total_bookings,
        "total_subscribers": total_subscribers,
        "total_queries": total_queries,
        "total_revenue": round(total_revenue, 2),
        "bookings_by_status": {
            "pending": pending_bookings,
            "confirmed": confirmed_bookings,
            "returned": returned_bookings,
            "cancelled": cancelled_bookings,
        },
    }


@router.get("/users", response_model=List[UserResponse])
def get_registered_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Retrieve details of all registered users."""
    return db.query(User).order_by(User.created_at.desc()).all()
