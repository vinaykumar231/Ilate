from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from auth.auth_bearer import JWTBearer
from db.session import get_db
from ..models import Video, Course, Subject, Standard
from ..schemas import VideoCreate
import os



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

base_url_path = "http://192.168.29.40:8000"



# Define the post method to upload videos
@router.post("/videos/", response_model=None)
def create_video(course_name: str, subject_name: str, standard_name: str, name: str, video_file: UploadFile = File(...),
                 db: Session = Depends(get_db), token: str = Depends(JWTBearer())):

    try:
        course_id = get_course_id(course_name, db)
        subject_id = get_subject_id(subject_name, db)
        standard_id = get_standard_id(standard_name, db)

        # Define the path to save the video file
        file_location = f"static/uploads/{video_file.filename}"

        # Save the file to the "static/uploads" directory
        with open(file_location, "wb") as buffer:
            buffer.write(video_file.file.read())

        # Create the new video record
        new_video = Video(name=name, url=file_location, course_id=course_id,
                          standard_id=standard_id, subject_id=subject_id)

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

@router.put("/videos/{video_id}", response_model=None)
def update_video(video_id: int, name: str, video_file: UploadFile = File(None), db: Session = Depends(get_db)):
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
            with open(f"uploads/{video_file.filename}", "wb") as buffer:
                buffer.write(video_file.file.read())
            db_video.url = f"uploads/{video_file.filename}"

        # Automatically fetch subject ID, standard ID, and course ID from the video object
        subject_id = db_video.subject_id
        standard_id = db_video.standard_id
        course_id = db_video.course_id

        db.commit()
        db.refresh(db_video)
        return db_video
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.delete("/videos/{video_id}")
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