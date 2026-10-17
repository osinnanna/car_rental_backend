from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from models.testimonial import Testimonial
from schemas.testimonial import (
    TestimonialCreate,
    TestimonialStatusUpdate,
    TestimonialResponse,
)
from core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])


@router.get("", response_model=List[TestimonialResponse])
def get_active_testimonials(db: Session = Depends(get_db)):
    """Public: Retrieve all approved and active customer testimonials."""
    return (
        db.query(Testimonial)
        .filter(Testimonial.status == "Active")
        .order_by(Testimonial.created_at.desc())
        .all()
    )


@router.post("", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
def post_testimonial(
    testimonial_in: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Authenticated User: Submit a new testimonial (defaults to Inactive pending admin approval)."""
    testimonial = Testimonial(
        user_id=current_user.id,
        content=testimonial_in.content,
        status="Inactive",
    )
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.get("/all", response_model=List[TestimonialResponse])
def get_all_testimonials_admin(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Retrieve all testimonials for moderation."""
    return db.query(Testimonial).order_by(Testimonial.created_at.desc()).all()


@router.put("/{testimonial_id}/status", response_model=TestimonialResponse)
def update_testimonial_status(
    testimonial_id: int,
    status_in: TestimonialStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Moderate testimonial (set status to Active or Inactive)."""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")

    testimonial.status = status_in.status
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Delete a testimonial."""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")

    db.delete(testimonial)
    db.commit()
    return None
