from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import uuid
from middleware.auth import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

# Ensure upload directory exists
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile):
    """Validate file extension and size"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")
        
    file_extension = Path(file.filename or "").suffix.lower()
    
    if file_extension in ALLOWED_IMAGE_EXTENSIONS:
        max_size = MAX_IMAGE_SIZE
        file_type = "image"
    elif file_extension in ALLOWED_DOCUMENT_EXTENSIONS:
        max_size = MAX_DOCUMENT_SIZE
        file_type = "document"
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed: {file.filename}. Allowed types: images ({', '.join(ALLOWED_IMAGE_EXTENSIONS)}) or documents ({', '.join(ALLOWED_DOCUMENT_EXTENSIONS)})"
        )
    
    # Validate file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > max_size:
        raise HTTPException(
            status_code=400, 
            detail=f"File too large: {file.filename}. Maximum size is {max_size / (1024*1024)} MB"
        )
    
    return file_type

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a single image or document file
    """
    # Only sellers and admins can upload files
    if current_user["role"] not in ["seller", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to upload files")
    
    # Validate file
    file_type = validate_file(file)
    
    # Generate unique filename
    file_extension = Path(file.filename or "").suffix.lower()
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Return URL to access the file
    file_url = f"/uploads/{filename}"
    return {"url": file_url, "filename": filename, "type": file_type}

@router.post("/images/bulk")
async def upload_multiple_images(
    files: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload multiple image or document files
    """
    # Only sellers and admins can upload files
    if current_user["role"] not in ["seller", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to upload files")
    
    uploaded_files = []
    
    for file in files:
        # Validate file
        file_type = validate_file(file)
        
        # Generate unique filename
        file_extension = Path(file.filename or "").suffix.lower()
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Store file info
        file_url = f"/uploads/{filename}"
        uploaded_files.append({
            "url": file_url, 
            "filename": filename,
            "type": file_type,
            "original_name": file.filename
        })
    
    return {"files": uploaded_files}

# Serve uploaded files
from fastapi.staticfiles import StaticFiles