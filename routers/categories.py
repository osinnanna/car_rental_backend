from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.car import Category
from schemas.car import CategoryCreate, CategoryUpdate, CategoryResponse
from core.deps import get_current_admin

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Retrieve all categories (for 'Explore by Category' section)."""
    return db.query(Category).order_by(Category.name.asc()).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a single category."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Create a new car category."""
    existing = db.query(Category).filter((Category.name == cat_in.name) | (Category.slug == cat_in.slug)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name or slug already exists")

    category = Category(
        name=cat_in.name,
        slug=cat_in.slug,
        description=cat_in.description,
        image_url=cat_in.image_url,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Update an existing category."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if cat_in.name is not None:
        category.name = cat_in.name
    if cat_in.slug is not None:
        category.slug = cat_in.slug
    if cat_in.description is not None:
        category.description = cat_in.description
    if cat_in.image_url is not None:
        category.image_url = cat_in.image_url

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Admin: Delete a category."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
    return None
