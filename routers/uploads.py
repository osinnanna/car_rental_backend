import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from core.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/upload", tags=["File Uploads"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".svg"}


@router.post("/image")
def upload_image(
    file: UploadFile = File(...),
    folder: str = Form("cars"),  # cars, brands, avatars, categories
    current_user: User = Depends(get_current_user),
):
    """Upload an image file (cars, brands, avatars, categories)."""
    # Sanitize folder name
    clean_folder = "".join(c for c in folder if c.isalnum() or c in ("-", "_"))
    target_dir = os.path.join(UPLOAD_DIR, clean_folder)
    os.makedirs(target_dir, exist_ok=True)

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Generate unique filename
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(target_dir, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    relative_url = f"/uploads/{clean_folder}/{unique_name}"
    return {
        "filename": unique_name,
        "url": relative_url,
        "content_type": file.content_type,
    }
