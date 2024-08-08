from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request , Form
from sqlalchemy.orm import Session
from auth.auth_bearer import JWTBearer
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher
from db.session import get_db
from ..models import Video, Course, Subject, Standard
from ..schemas import VideoCreate
import os
from typing import Optional, List
import os
import uuid
import shutil
from dotenv import load_dotenv


load_dotenv()
router = APIRouter()

def get_course_id(course_name: str, db: Session):
    course = db.query(Course).filter(Course.name == course_name).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.id

def get_subject_id(subject_name: str, db: Session):
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject.id

def get_standard_id(standard_name: str, db: Session):
    standard = db.query(Standard).filter(Standard.name == standard_name).first()
    if not standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    return standard.id

base_url_path = os.getenv("BASE_URL_PATH")


def save_upload_file(upload_file: UploadFile) -> str:
    try:
        unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
        file_path = os.path.join("static", "uploads", unique_filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        file_path = file_path.replace("\\", "/")
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.post("/videos/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def create_video(
    course_name:str = Form(...),
    subject_name: str = Form(None),
    standard_name: str = Form(None),
    name: str = Form(None),
    video_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(JWTBearer())
):
    try:
        course_id = get_course_id(course_name, db)
        subject_id = get_subject_id(subject_name, db)
        standard_id = get_standard_id(standard_name, db)

        file_location = save_upload_file(video_file)

        new_video = Video(
            name=name,
            url=file_location,
            course_id=course_id,
            standard_id=standard_id,
            subject_id=subject_id
        )

        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        return new_video
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert demo video: {str(e)}")

@router.get("/videos", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_all_videos( db: Session = Depends(get_db)):
    try:
        course = db.query(Course).first()
        standard = db.query(Standard).first()
        subject = db.query(Subject).first()
        
        videos = db.query(Video).all()
        
        video_list = []
        for video in videos:
            video_url = f"{base_url_path}/{video.url}"
    
            video_data = {
                "course_name":course.name,
                "standard_name":standard.name,
                "subject_name":subject.name,
                "name": video.name,
                "url": video_url,
                "subject_id": video.subject_id,
                "id": video.id,
                "course_id": video.course_id,
                "standard_id": video.standard_id
            }
            video_list.append(video_data)
        
        return video_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get videos: {str(e)}")
##############################################################################

def save_upload(file_path: str) -> str:
    try:
        unique_filename = str(uuid.uuid4()) + "_" + os.path.basename(file_path)
        dest_path = os.path.join("static", "uploads", unique_filename)
        
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        shutil.copyfile(file_path, dest_path)
        
        dest_path = dest_path.replace("\\", "/")
        return dest_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.get("/videos_by_criteria/", response_model=None)
def get_videos_by_criteria(
    course_name: Optional[str] = None,
    standard_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        result = {}
        base_url_path = os.getenv("BASE_URL_PATH")
        
        query = db.query(Video)
        
        if not course_name:
            courses = db.query(Course).all()
            result["courses"] = [{"id": c.id, "name": c.name} for c in courses]
        
        if course_name and not standard_id:
            course = db.query(Course).filter(Course.name == course_name).first()
            if course:
                standards = db.query(Standard).filter(Standard.course_id == course.id).all()
                result["standards"] = [{"id": s.id, "name": s.name} for s in standards]
        
        if standard_id and not subject_id:
            subjects = db.query(Subject).filter(Subject.standard_id == standard_id).all()
            result["subjects"] = [{"id": s.id, "name": s.name} for s in subjects]
        
        if subject_id:
            query = query.filter(Video.subject_id == subject_id)
        
        videos = query.all()
        if not videos:
            raise HTTPException(status_code=404, detail="Videos not found")
        
        video_data = []
        for video in videos:
            video_path = save_upload(video.url)
            video_url = f"{base_url_path}/{video_path}"
            video_info = {
                "name": video.name,
                "url": video_url,
            }
            video_data.append(video_info)
        
        result["videos"] = video_data
        return result
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get demo video: {str(e)}")

##############################################################################
@router.get("/videos/", response_model=None, dependencies=[Depends(JWTBearer())])
def get_videos(course_name: str, standard_name: str, subject_name: str, db: Session = Depends(get_db)):
    try:
        course_id = get_course_id(course_name, db)
        subject_id = get_subject_id(subject_name, db)
        standard_id = get_standard_id(standard_name, db)
    except HTTPException as e:
        raise (f"Failed to get demo video: {str(e)}")

    videos = db.query(Video).filter(
        Video.course_id == course_id,
        Video.standard_id == standard_id,
        Video.subject_id == subject_id
    ).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")

    video_data = []
    for video in videos:
        video_url = f"{base_url_path}/{video.url}"  
        video_info = {
            "name": video.name,
            "url": video_url,
            "subject_id": video.subject_id,
            "id": video.id,
            "course_id": video.course_id,
            "standard_id": video.standard_id
        }
        video_data.append(video_info)

    return video_data



@router.get("/videos/{video_id}", response_model=None)
def get_video(video_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        video_url = f"{base_url_path}/{video.url}"
        print(video_url)

        video_data = {
            "name": video.name,
            "url": video_url,
            "subject_id": video.subject_id,
            "id": video.id,
            "course_id": video.course_id,
            "standard_id": video.standard_id
        }

        return video_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get demo video: {str(e)}")

@router.put("/videos/{video_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def update_video(
    video_id: int,
    name: str,
    video_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        db_video = db.query(Video).filter(Video.id == video_id).first()
        if db_video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        if name:
            db_video.name = name

        if video_file:
            file_location = save_upload_file(video_file)
            db_video.url = file_location

        subject_id = db_video.subject_id
        standard_id = db_video.standard_id
        course_id = db_video.course_id

        db.commit()
        db.refresh(db_video)

        return {"message": "Video and file updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update demo video: {str(e)}")

    
@router.delete("/videos/{video_id}", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def delete_video(video_id: int, db: Session = Depends(get_db)):
    try:
        db_video = db.query(Video).filter(Video.id == video_id).first()
        if db_video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        filename = db_video.url.split("/")[-1]

        file_path = f"uploads/{filename}"

        if os.path.exists(file_path):
            os.remove(file_path)
            db.delete(db_video)
            db.commit()
            return {"message": "Video and file deleted successfully"}
        else:
            db.delete(db_video)
            db.commit()
            return {"message": "Video deleted successfully, but file not found"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete demo video: {str(e)}")