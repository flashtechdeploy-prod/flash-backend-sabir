import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.upload_helper import upload_file_with_prefix
from app.models.hr.employee import Employee
from app.models.hr.employee_document import EmployeeDocument
from app.schemas.hr.employee_document import EmployeeDocumentOut


router = APIRouter()


# All uploads now go to Supabase Storage


@router.get("/by-db-id/{employee_db_id}/documents", response_model=List[EmployeeDocumentOut])
async def list_employee_documents(employee_db_id: int, db: Session = Depends(get_db)) -> List[EmployeeDocumentOut]:
    emp = db.query(Employee).filter(Employee.id == employee_db_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    docs = (
        db.query(EmployeeDocument)
        .filter(EmployeeDocument.employee_db_id == employee_db_id)
        .order_by(EmployeeDocument.id.desc())
        .all()
    )

    out: List[EmployeeDocumentOut] = []
    for d in docs:
        # All URLs are from Supabase Storage
        url = d.path
        out.append(
            EmployeeDocumentOut(
                id=d.id,
                employee_db_id=d.employee_db_id,
                name=d.name,
                filename=d.filename,
                url=url,
                mime_type=d.mime_type,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
        )
    return out


@router.post("/by-db-id/{employee_db_id}/documents", response_model=EmployeeDocumentOut)
async def upload_employee_document(
    employee_db_id: int,
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> EmployeeDocumentOut:
    emp = db.query(Employee).filter(Employee.id == employee_db_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not name.strip():
        raise HTTPException(status_code=400, detail="Document name is required")

    ct = file.content_type or "application/octet-stream"
    content = await file.read()

    # Upload to Supabase Storage
    url, new_filename = await upload_file_with_prefix(
        content=content,
        original_filename=file.filename or "",
        prefix=f"emp_{employee_db_id}",
        content_type=ct,
        subdir=f"employees/{employee_db_id}",
    )

    doc = EmployeeDocument(
        employee_db_id=employee_db_id,
        name=name.strip(),
        filename=file.filename or new_filename,
        path=url,  # Store the full URL (B2) or local path
        mime_type=ct,
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return EmployeeDocumentOut(
        id=doc.id,
        employee_db_id=doc.employee_db_id,
        name=doc.name,
        filename=doc.filename,
        url=url,
        mime_type=doc.mime_type,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


@router.delete("/by-db-id/{employee_db_id}/documents/{doc_id}")
async def delete_employee_document(employee_db_id: int, doc_id: int, db: Session = Depends(get_db)) -> dict:
    doc = (
        db.query(EmployeeDocument)
        .filter(EmployeeDocument.id == doc_id)
        .filter(EmployeeDocument.employee_db_id == employee_db_id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Files are stored in Supabase - no local deletion needed

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted"}


@router.post("/by-db-id/{employee_db_id}/profile-photo")
async def upload_profile_photo(
    employee_db_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    """Upload or update employee profile photo."""
    emp = db.query(Employee).filter(Employee.id == employee_db_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    ct = file.content_type or "image/jpeg"
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await file.read()

    # Upload to cloud storage
    url, new_filename = await upload_file_with_prefix(
        content=content,
        original_filename=file.filename or "profile.jpg",
        prefix=f"profile_{employee_db_id}",
        content_type=ct,
        subdir=f"employees/{employee_db_id}/profile",
    )

    # Update employee profile_photo field
    emp.profile_photo = url
    db.commit()
    db.refresh(emp)

    return {"url": url, "message": "Profile photo updated successfully"}
