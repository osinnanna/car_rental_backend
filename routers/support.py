from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from models.support import FAQ
from models.booking import Booking
from schemas.support import (
    FAQCreate,
    FAQUpdate,
    FAQResponse,
    SupportQueryRequest,
    SupportQueryResponse,
)
from core.deps import get_current_admin, get_optional_current_user

router = APIRouter(prefix="/support", tags=["Support"])


@router.get("/faqs", response_model=List[FAQResponse])
def get_faqs(
    category: Optional[str] = Query(None, description="Filter FAQs by category"),
    db: Session = Depends(get_db),
):
    """Public: Retrieve frequently asked questions (FAQs)."""
    query = db.query(FAQ)
    if category:
        query = query.filter(FAQ.category.ilike(category))
    return query.order_by(FAQ.id.asc()).all()


@router.get("/faqs/{faq_id}", response_model=FAQResponse)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a specific FAQ."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")
    return faq


@router.post("/ask", response_model=SupportQueryResponse)
def ask_support(
    request: SupportQueryRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Answer customer questions instantly using the FAQ knowledgebase and user context (Zero tokens)."""
    q = request.query.strip().lower()

    # 1. Check if user is asking about their personal reservations
    if "booking" in q or "reservation" in q or "check my booking" in q:
        if not current_user:
            return SupportQueryResponse(
                query=request.query,
                answer="To check your reservations, please log in to your account. Once logged in, your full history is visible on the 'Booking History' page.",
                suggestions=["Log in to account", "How do I book a car?", "Cancellation policy"],
            )
        recent_bookings = (
            db.query(Booking)
            .filter(Booking.user_id == current_user.id)
            .order_by(Booking.created_at.desc())
            .limit(3)
            .all()
        )
        if not recent_bookings:
            return SupportQueryResponse(
                query=request.query,
                answer=f"Hi {current_user.full_name}, you currently have no recent bookings. Browse our fleet under 'Browse Cars' to reserve your next ride!",
                suggestions=["Browse Cars", "Rental requirements", "Pricing & rates"],
            )
        summaries = [
            f"• {b.car.title if b.car else 'Vehicle'} ({b.status}) from {b.from_date.strftime('%d %b %Y')} to {b.to_date.strftime('%d %b %Y')}"
            for b in recent_bookings
        ]
        answer_text = f"Here are your latest bookings, {current_user.full_name}:\n" + "\n".join(summaries)
        return SupportQueryResponse(
            query=request.query,
            answer=answer_text,
            suggestions=["Modify my reservation", "Return policy", "Contact human support"],
        )

    # 2. Search the FAQ knowledgebase
    all_faqs = db.query(FAQ).all()
    matched_faq = None
    best_score = 0

    query_words = set(q.split())
    for faq in all_faqs:
        faq_text = f"{faq.question} {faq.answer} {faq.category}".lower()
        faq_words = set(faq_text.split())
        overlap = len(query_words.intersection(faq_words))

        # Check exact phrase or high overlap
        if q in faq.question.lower():
            matched_faq = faq
            break
        elif overlap > best_score:
            best_score = overlap
            matched_faq = faq

    if matched_faq and (best_score >= 1 or q in matched_faq.question.lower()):
        return SupportQueryResponse(
            query=request.query,
            answer=matched_faq.answer,
            matched_faq=FAQResponse.model_validate(matched_faq),
            suggestions=["Check my booking", "Rental requirements", "Contact support"],
        )

    # 3. Helpful fallback
    return SupportQueryResponse(
        query=request.query,
        answer=(
            "Thank you for contacting FAST CARS Support. For immediate assistance with this topic, "
            "you can reach our team directly at support@fastcars.com or call +234 800 FAST CARS."
        ),
        suggestions=[
            "Check my booking",
            "Rental requirements",
            "Payment methods",
            "Cancellation policy",
        ],
    )


# --- ADMIN FAQ MANAGEMENT ---

@router.post("/faqs", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def create_faq(
    faq_in: FAQCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Add a new FAQ to the knowledgebase."""
    faq = FAQ(
        question=faq_in.question,
        answer=faq_in.answer,
        category=faq_in.category,
    )
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


@router.put("/faqs/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    faq_in: FAQUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update an existing FAQ."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")

    if faq_in.question is not None:
        faq.question = faq_in.question
    if faq_in.answer is not None:
        faq.answer = faq_in.answer
    if faq_in.category is not None:
        faq.category = faq_in.category

    db.commit()
    db.refresh(faq)
    return faq


@router.delete("/faqs/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Delete an FAQ."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")

    db.delete(faq)
    db.commit()
    return None
