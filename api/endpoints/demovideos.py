from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_bearer import JWTBearer
from db.session import get_db
from ..models import Video, Course, Subject, Standard
from ..schemas import VideoCreate

router = APIRouter()


def get_course_id(course_name: str, db: Session):
    course = db.query(Course).filter(Course.name == course_name).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.id

# Function to get subject ID by name
def get_subject_id(subject_name: str, db: Session):
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject.id

# Function to get standard ID by name
def get_standard_id(standard_name: str, db: Session):
    standard = db.query(Standard).filter(Standard.name == standard_name).first()
    if not standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    return standard.id

@router.post("/videos/", response_model=None, dependencies=[Depends(JWTBearer())])
def create_video(video: VideoCreate, course_name: str, subject_name: str, standard_name: str,
                 db: Session = Depends(get_db)):
    course_id = get_course_id(course_name, db)
    subject_id = get_subject_id(subject_name, db)
    standard_id = get_standard_id(standard_name, db)

    db_video = Video(**video.dict(), course_id=course_id, standard_id=standard_id, subject_id=subject_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


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

    return videos
