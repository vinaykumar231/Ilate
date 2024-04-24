from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from auth.auth_bearer import JWTBearer, get_current_user, get_admin
from ..models import DemoFormFill, LmsUsers
from ..schemas import DemoformfillCreate


router = APIRouter()




@router.post("/demoformfill/", response_model=None, dependencies=[Depends(JWTBearer())])
def create_demoformfill(demo_form: DemoformfillCreate, current_user:LmsUsers = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    demo_form.user_id = current_user.user_id
    db_demoformfill = DemoFormFill(**demo_form.dict())
    db.add(db_demoformfill)
    db.commit()
    db.refresh(db_demoformfill)
    return db_demoformfill


@router.get("/demoformfill/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def read_demoformfill(db: Session = Depends(get_db)):
    db_demoformfill = db.query(DemoFormFill).all()
    if db_demoformfill is None:
        raise HTTPException(status_code=404, detail="Demoformfill not found")
    return db_demoformfill


# def get_demo_videos(db: Session, course_id: int, subject_id: int, standard_id: int) -> List[Dict[str, str]]:
#     course = db.query(Course).filter(Course.id == course_id).first()
#     subject = db.query(Subject).filter(Subject.id == subject_id, Subject.course_id == course_id).first()
#     standard = db.query(Standard).filter(Standard.id == standard_id, Standard.subject_id == subject_id).first()
#
#     if not course or not subject or not standard:
#         return []
#
#     demo_videos = db.query(DemoVideo).filter(
#         DemoVideo.course_id == course.id,
#         DemoVideo.subject_id == subject.id,
#         DemoVideo.standard_id == standard.id
#     ).all()
#
#     demo_videos_list = [{"title": video.title, "url": video.url} for video in demo_videos]
#
#     return demo_videos_list
