from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from models.car import Car
from models.wishlist import Wishlist
from schemas.wishlist import WishlistCreate, WishlistResponse
from core.deps import get_current_user

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("", response_model=List[WishlistResponse])
def get_user_wishlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all cars saved in the current user's wishlist."""
    return (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id)
        .order_by(Wishlist.created_at.desc())
        .all()
    )


@router.get("/count")
def get_wishlist_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the current count of items in the user's wishlist (for the header badge)."""
    count = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).count()
    return {"count": count}


@router.post("", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    item_in: WishlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a car to the user's wishlist."""
    car = db.query(Car).filter(Car.id == item_in.car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    existing = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id, Wishlist.car_id == item_in.car_id)
        .first()
    )
    if existing:
        return existing

    wishlist_item = Wishlist(user_id=current_user.id, car_id=item_in.car_id)
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


@router.post("/toggle/{car_id}")
def toggle_wishlist(
    car_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Toggle a car in or out of the user's wishlist (ideal for the UI heart button)."""
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    existing = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id, Wishlist.car_id == car_id)
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        in_wishlist = False
    else:
        new_item = Wishlist(user_id=current_user.id, car_id=car_id)
        db.add(new_item)
        db.commit()
        in_wishlist = True

    total_count = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).count()
    return {"in_wishlist": in_wishlist, "total_count": total_count}


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    car_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a car from the user's wishlist."""
    item = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == current_user.id, Wishlist.car_id == car_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not in wishlist")

    db.delete(item)
    db.commit()
    return None
