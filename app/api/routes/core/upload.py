import os

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.core.file import File as FileModel
from app.schemas.core.file import FileResponse
from app.api.dependencies import get_current_user
from app.models.core.user import User
from app.core.upload_helper import upload_file_with_prefix

router = APIRouter()


@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query("uploads", description="Folder to upload to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file and return its URL.
    Stores file in Supabase Storage and saves metadata to the database.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Determine MIME type if missing
        mime_type = file.content_type or "application/octet-stream"
        
        # Upload to Supabase Storage
        public_url, new_filename = await upload_file_with_prefix(
            content=content,
            original_filename=file.filename,
            prefix="file",
            content_type=mime_type,
            subdir=folder,
        )
        
        # Save to database
        db_file = FileModel(
            filename=file.filename,
            unique_filename=new_filename,
            path=public_url,
            storage_type="local",
            mime_type=mime_type,
            size=len(content),
            user_id=current_user.id
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/storage/status")
async def storage_status():
    """Check the status of storage configuration."""
    return {
        "storage_type": "local",
        "uploads_dir": settings.UPLOADS_DIR,
        "message": "Using local file storage.",
    }

