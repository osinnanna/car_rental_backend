from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.contact import ContactQuery, Subscriber
from schemas.contact import (
    ContactQueryCreate,
    ContactQueryStatusUpdate,
    ContactQueryResponse,
    SubscriberCreate,
    SubscriberResponse,
)
from core.deps import get_current_admin

router = APIRouter(prefix="/contact", tags=["Contact & Newsletter"])


@router.post("", response_model=ContactQueryResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_query(
    query_in: ContactQueryCreate,
    db: Session = Depends(get_db),
):
    """Guest/Customer: Submit an inquiry through the Contact Us form."""
    query_obj = ContactQuery(
        name=query_in.name,
        email=query_in.email,
        phone_number=query_in.phone_number,
        message=query_in.message,
        status="Pending",
    )
    db.add(query_obj)
    db.commit()
    db.refresh(query_obj)
    return query_obj


@router.post("/subscribe", response_model=SubscriberResponse, status_code=status.HTTP_201_CREATED)
def subscribe_newsletter(
    sub_in: SubscriberCreate,
    db: Session = Depends(get_db),
):
    """Guest/Customer: Subscribe email address to the newsletter."""
    existing = db.query(Subscriber).filter(Subscriber.email == sub_in.email).first()
    if existing:
        return existing

    sub = Subscriber(email=sub_in.email)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


# --- ADMIN ENDPOINTS ---

@router.get("/queries", response_model=List[ContactQueryResponse])
def get_all_queries_admin(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Retrieve all customer contact inquiries."""
    return db.query(ContactQuery).order_by(ContactQuery.created_at.desc()).all()


@router.put("/queries/{query_id}/status", response_model=ContactQueryResponse)
def update_query_status(
    query_id: int,
    status_in: ContactQueryStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update contact query status (Pending, Read, Responded)."""
    query_obj = db.query(ContactQuery).filter(ContactQuery.id == query_id).first()
    if not query_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")

    query_obj.status = status_in.status
    db.commit()
    db.refresh(query_obj)
    return query_obj


@router.delete("/queries/{query_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_query(
    query_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Delete a contact query."""
    query_obj = db.query(ContactQuery).filter(ContactQuery.id == query_id).first()
    if not query_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")

    db.delete(query_obj)
    db.commit()
    return None


@router.get("/subscribers", response_model=List[SubscriberResponse])
def get_all_subscribers_admin(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Retrieve the list of all newsletter subscribers."""
    return db.query(Subscriber).order_by(Subscriber.created_at.desc()).all()


@router.delete("/subscribers/{subscriber_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Remove a subscriber from the newsletter list."""
    sub = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscriber not found")

    db.delete(sub)
    db.commit()
    return None
