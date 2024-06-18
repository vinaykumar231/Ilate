from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from auth.auth_bearer import JWTBearer, get_admin,get_admin_student_teacher_parent
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
from ..models.announcement import Announcement
from typing import Optional

router = APIRouter()

def save_upload_file(upload_file: Optional[UploadFile]) -> Optional[str]:
    if not upload_file:
        return None
    
    try:
        unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
        file_path = os.path.join("static", "uploads", unique_filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        # Convert backslashes to forward slashes
        file_path = file_path.replace("\\", "/")
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.post("/announcement/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def create_content(
    title: str = Form(...),
    announcement_text: str = Form(None),
    announcement_images: UploadFile = File(default=None),
    db: Session = Depends(get_db)
):
    announcement_images_path = save_upload_file(announcement_images)
    try:
        # Create a new Announcement object
        db_announcement = Announcement(
            title=title,
            announcement_text=announcement_text,
            announcement_images=announcement_images_path
        )

        db.add(db_announcement)
        db.commit()
        db.refresh(db_announcement)

        return db_announcement 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/announcement/{announcement_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_student_teacher_parent)])
async def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    base_url_path = "http://192.168.29.82:8001"  # Your base URL path

    announcement_images_path = announcement.announcement_images
    if announcement_images_path:
        announcement_images_url = f"{base_url_path}/{announcement_images_path}"
    else:
        announcement_images_url = None

    announcement_response = Announcement(
        id=announcement.id,
        title=announcement.title,
        announcement_text=announcement.announcement_text,
        announcement_images=announcement_images_url
    )

    return announcement_response

@router.put("/announcement/{announcement_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def update_announcement(
    announcement_id: int,
    title: str = Form(...),
    announcement_text: str = Form(None),
    announcement_images: UploadFile = File(default=None),
    db: Session = Depends(get_db)
):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement_images_path = announcement.announcement_images
    if announcement_images:
        announcement_images_path = save_upload_file(announcement_images)

    try:
        announcement.title = title
        announcement.announcement_text = announcement_text
        announcement.announcement_images = announcement_images_path
        db.commit()
        db.refresh(announcement)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    base_url_path = "http://192.168.29.82:8001"  # Your base URL path
    announcement_images_url = f"{base_url_path}/{announcement_images_path}" if announcement_images_path else None

    announcement_response = Announcement(
        id=announcement.id,
        title=announcement.title,
        announcement_text=announcement.announcement_text,
        announcement_images=announcement_images_url
    )

    return announcement_response

@router.delete("/announcement/{announcement_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    try:
        db.delete(announcement)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Announcement deleted successfully"}