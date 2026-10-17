from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.page import Page
from schemas.page import PageCreate, PageUpdate, PageResponse
from core.deps import get_current_admin

router = APIRouter(prefix="/pages", tags=["CMS Pages"])


@router.get("", response_model=List[PageResponse])
def get_all_pages(db: Session = Depends(get_db)):
    """Retrieve all available CMS content pages."""
    return db.query(Page).all()


@router.get("/{page_type}", response_model=PageResponse)
def get_page_by_type(page_type: str, db: Session = Depends(get_db)):
    """Retrieve content of a specific page (e.g. aboutus, privacy, terms, contactinfo)."""
    page = db.query(Page).filter(Page.page_type == page_type.lower()).first()
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    return page


@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(
    page_in: PageCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Create a new CMS page."""
    existing = db.query(Page).filter(Page.page_type == page_in.page_type.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page already exists")

    page = Page(
        page_type=page_in.page_type.lower(),
        title=page_in.title,
        content=page_in.content,
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.put("/{page_type}", response_model=PageResponse)
def update_page_content(
    page_type: str,
    page_in: PageUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update content or title of a CMS page."""
    page = db.query(Page).filter(Page.page_type == page_type.lower()).first()
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    if page_in.title is not None:
        page.title = page_in.title
    if page_in.content is not None:
        page.content = page_in.content

    db.commit()
    db.refresh(page)
    return page
