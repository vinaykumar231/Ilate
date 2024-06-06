from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
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

base_url_path = "http://192.168.29.82:8001"



# Define the post method to upload videos
def save_upload_file(upload_file: UploadFile) -> str:
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

@router.post("/videos/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def create_video(
    course_name: str,
    subject_name: str,
    standard_name: str,
    name: str,
    video_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(JWTBearer())
):
    try:
        course_id = get_course_id(course_name, db)
        subject_id = get_subject_id(subject_name, db)
        standard_id = get_standard_id(standard_name, db)

        # Save the video file
        file_location = save_upload_file(video_file)

        # Create the new video record
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
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/videos/", response_model=None)
# def get_all_videos(db: Session = Depends(get_db)):
#     try:
#         videos = db.query(Video).all()
#         return videos
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
##############################################################################

def save_upload(files: List[str], base_url_path: str) -> List[str]:
    file_paths = []
    try:
        for file_path in files:
            unique_filename = str(uuid.uuid4()) + "_" + os.path.basename(file_path)
            dest_path = os.path.join(base_url_path, unique_filename)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            shutil.copyfile(file_path, dest_path)
        
            # Convert backslashes to forward slashes
            dest_path = dest_path.replace("\\", "/")
            file_paths.append(dest_path)
        return file_paths
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
        base_url_path = "static/uploads"
        base_url_http_path = "http://192.168.29.82:8001/static/uploads"
        query = db.query(Video)

        if not course_name:
            courses = db.query(Course).all()
            result["courses"] = [{"id": c.id, "name": c.name} for c in courses]

        course = db.query(Course).filter(Course.name == course_name).first()
        if course_name and not standard_id:
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
            video_url = f"{base_url_http_path}/{os.path.basename(video.url)}"
            video_info = {
                "name": video.name,
                "url": video_url,
            }
            video_data.append(video_info)

        return {
            "videos": video_data,
            
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##############################################################################
@router.get("/videos/", response_model=None, dependencies=[Depends(JWTBearer())])
def get_videos(course_name: str, standard_name: str, subject_name: str, db: Session = Depends(get_db)):
    try:
        course_id = get_course_id(course_name, db)
        subject_id = get_subject_id(subject_name, db)
        standard_id = get_standard_id(standard_name, db)
    except HTTPException as e:
        raise e

    videos = db.query(Video).filter(
        Video.course_id == course_id,
        Video.standard_id == standard_id,
        Video.subject_id == subject_id
    ).all()
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")

    video_data = []
    for video in videos:
        video_url = f"{base_url_path}/{video.url}"  # Assuming base_url_path is defined somewhere
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

        # Build the full URL for the video
        video_url = f"{base_url_path}/{video.url}"
        print(video_url)

        # Modify the video URL for the response
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
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/videos/{video_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def update_video(
    video_id: int,
    name: str,
    video_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Fetch the video details from the database based on the provided video ID
        db_video = db.query(Video).filter(Video.id == video_id).first()
        if db_video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        # Update the name if provided
        if name:
            db_video.name = name

        # Update the video file if provided
        if video_file:
            file_location = save_upload_file(video_file)
            db_video.url = file_location

        # Fetch subject ID, standard ID, and course ID
        subject_id = db_video.subject_id
        standard_id = db_video.standard_id
        course_id = db_video.course_id

        # Commit changes to the database
        db.commit()
        # Refresh the video object
        db.refresh(db_video)

        # Return updated video details along with subject ID, standard ID, and course ID
        return {"message": "Video and file updated successfully"}
    
    except Exception as e:
        # If any error occurs, raise HTTPException with status code 500
        raise HTTPException(status_code=500, detail=str(e))

    
@router.delete("/videos/{video_id}", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def delete_video(video_id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve the video from the database
        db_video = db.query(Video).filter(Video.id == video_id).first()
        if db_video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        # Get the filename from the Video instance
        filename = db_video.url.split("/")[-1]

        # Construct the file path
        file_path = f"uploads/{filename}"

        # Check if the file exists and delete it if found
        if os.path.exists(file_path):
            os.remove(file_path)
            db.delete(db_video)
            db.commit()
            return {"message": "Video and file deleted successfully"}
        else:
            # If file not found, delete the Video instance from the database
            db.delete(db_video)
            db.commit()
            return {"message": "Video deleted successfully, but file not found"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))