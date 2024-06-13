from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Course, Subject, Standard, Module, Lesson, Content
from ..schemas import CourseCreate, CourseUpdate
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher
from pydantic import BaseModel,  Field
from typing import Optional, List
from fastapi import UploadFile, File
from datetime import date
from enum import Enum
from sqlalchemy import JSON
import os
from urllib.parse import quote
import os
import uuid
import shutil


router = APIRouter()

##############################################################################################################################   
class CourseBase(BaseModel):
    name: str
    description: Optional[str]

class CourseCreate(CourseBase):
    pass

class StandardBase(BaseModel):
    name: str
    course_id: int

class StandardCreate(StandardBase):
    pass

class SubjectBase(BaseModel):
    name: str
    standard_id:int


class SubjectCreate(SubjectBase):
    pass

class ModuleBase(BaseModel):
    name: str
    subject_id:int

class ModuleCreate(ModuleBase):
    pass

class CourseCreateWithHierarchy(BaseModel):
    course: CourseCreate
    standards: List[StandardCreate]
    subjects: List[SubjectCreate]
    modules: List[ModuleCreate]
##############################################################################################################################

@router.post("/courses_create/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def create_course_with_hierarchy(course_data: CourseCreateWithHierarchy, db: Session = Depends(get_db)):
    try:
        # Create course
        course = Course(name=course_data.course.name, description=course_data.course.description)
        db.add(course)
        db.commit()
        db.refresh(course)

        # Create standards
        for standard_data in course_data.standards:
            standard = Standard(name=standard_data.name, course_id=course.id)
            db.add(standard)

        # Create subjects
        for subject_data in course_data.subjects:
            subject = Subject(name=subject_data.name, standard_id=subject_data.standard_id)
            db.add(subject)

        # Create modules
        for module_data in course_data.modules:
            module = Module(name=module_data.name, subject_id=module_data.subject_id)
            db.add(module)

        db.commit()

        return {"message": "Course hierarchy created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create course hierarchy: {str(e)}")
    
def build_course_hierarchy(course_id: int, db: Session) -> CourseCreateWithHierarchy:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    standards = db.query(Standard).filter(Standard.course_id == course_id).all()
    subjects = []
    for standard in standards:
        subjects.extend(db.query(Subject).filter(Subject.standard_id == standard.id).all())
    
    modules = []
    for subject in subjects:
        modules.extend(db.query(Module).filter(Module.subject_id == subject.id).all())

    course_hierarchy = CourseCreateWithHierarchy(
        course=CourseCreate(name=course.name, description=course.description),
        standards=[StandardCreate(name=standard.name, course_id=standard.course_id) for standard in standards],
        subjects=[SubjectCreate(name=subject.name, standard_id=subject.standard_id) for subject in subjects],
        modules=[ModuleCreate(name=module.name, subject_id=module.subject_id) for module in modules]
    )

    return course_hierarchy
    
# @router.get("/courses_by_criteria/", response_model=List[CourseCreateWithHierarchy])
# def get_courses_by_criteria(
#     course_name: Optional[str] = None,
#     standard_id: Optional[int] = None,
#     subject_id: Optional[int] = None,
#     module_id: Optional[int] = None,
#     db: Session = Depends(get_db)
# ):
#     try:
#         query = db.query(Course)

#         if course_name:
#             query = query.filter(Course.name == course_name)

#         if standard_id:
#             query = query.join(Standard, Standard.course_id == Course.id).filter(Standard.id == standard_id)

#         if subject_id:
#             query = query.join(Subject, Subject.standard_id == Standard.id).filter(Subject.id == subject_id)

#         if module_id:
#             query = query.join(Module, Module.subject_id == Subject.id).filter(Module.id == module_id)

#         courses = query.all()

#         if not courses:
#             raise HTTPException(status_code=404, detail="No courses found with the given criteria")

#         course_hierarchies = [build_course_hierarchy(course.id, db) for course in courses]

#         return course_hierarchies

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# base_url_path = "http://192.168.29.40:8001"
# @router.get("/courses_by_criteria_with_content/", response_model=List[dict])
# def get_courses_by_criteria_with_content(
#     course_name: Optional[str] = None,
#     standard_id: Optional[int] = None,
#     subject_id: Optional[int] = None,
#     module_id: Optional[int] = None,
#     lesson_id: Optional[int] = None,
#     db: Session = Depends(get_db)
# ):
#     try:
#         query = db.query(Course)

#         if course_name:
#             query = query.filter(Course.name == course_name)
#         if standard_id:
#             query = query.join(Standard).filter(Standard.id == standard_id)
#         if subject_id:
#             query = query.join(Subject).filter(Subject.id == subject_id)
#         if module_id:
#             query = query.join(Module).filter(Module.id == module_id)
#         if lesson_id:
#             query = query.join(Lesson).filter(Lesson.lesson_id == lesson_id)

#         courses = query.all()
#         if not courses:
#             raise HTTPException(status_code=404, detail="No courses found with the given criteria")

#         course_hierarchies_with_content = []
#         for course in courses:
#             course_hierarchy = build_course_hierarchy(course.id, db)
#             lessons = db.query(Lesson).filter(Lesson.module_id.in_(
#                 [module.subject_id for module in course_hierarchy.modules])).all()

#             contents = []
#             for lesson in lessons:
#                 contents.extend(db.query(Content).filter(Content.lesson_id == lesson.lesson_id).all())

#             base_url_path = "http://192.168.29.40:8001"
#             content_data = [{
#                 "id": content.id,
#                 "name": content.name,
#                 "description": content.description,
#                 "content_type": content.content_type,
#                 "lesson_id": content.lesson_id,
#                 "content_paths": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
#             } for content in contents]

#             course_hierarchies_with_content.append({
#                 "course_hierarchy": course_hierarchy,
#                 "contents": content_data
#             })

#         return course_hierarchies_with_content

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



############################
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

@router.get("/filter_criteria/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_course_content_by_criteria(
    course_name: Optional[str] = None,
    standard_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    module_id: Optional[int] = None,
    lesson_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        result = {}
        base_url_path = "static/uploads"
        base_url_http_path = "http://192.168.29.82:8001/static/uploads"
        query = db.query(Content)

        if not course_name:
            courses = db.query(Course).all()
            result["courses"] = [{"id": c.id, "name": c.name} for c in courses]
            return result

        course = db.query(Course).filter(Course.name == course_name).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if course_name and not standard_id:
            standards = db.query(Standard).filter(Standard.course_id == course.id).all()
            result["standards"] = [{"id": s.id, "name": s.name} for s in standards]
            return result

        if standard_id and not subject_id:
            subjects = db.query(Subject).filter(Subject.standard_id == standard_id).all()
            result["subjects"] = [{"id": s.id, "name": s.name} for s in subjects]
            return result

        if subject_id and not module_id:
            modules = db.query(Module).filter(Module.subject_id == subject_id).all()
            result["modules"] = [{"id": m.id, "name": m.name} for m in modules]
            return result

        if module_id and not lesson_id:
            lessons = db.query(Lesson).filter(Lesson.module_id == module_id).all()
            result["lessons"] = [{"id": l.id, "name": l.name} for l in lessons]
            return result

        if lesson_id:
            query = query.filter(Content.lesson_id == lesson_id)

        content = query.all()
        if not content:
            raise HTTPException(status_code=404, detail="No content found with the given criteria")

        content_data = []
        for c in content:
            # Collect all paths to save
            paths_to_save = c.content_path

            # Save files and get their new paths
            saved_paths = save_upload(paths_to_save, base_url_path)

            # Convert to URL paths
            url_paths = [f"{base_url_http_path}/{os.path.basename(path)}" for path in saved_paths]

            content_data.append({
                "name": c.name,
                "description": c.description,
                "content_type": c.content_type,
                "content_paths": url_paths  # Use the new saved paths with UUIDs
            })

        return content_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

######
@router.get("/courses_hierarchy/{course_id}", response_model=CourseCreateWithHierarchy, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_course_hierarchy(course_id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve the course
        course = db.query(Course).filter(Course.id == course_id).first()

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Retrieve standards
        standards = db.query(Standard).filter(Standard.course_id == course_id).all()

        # Retrieve subjects
        subjects = []
        for standard in standards:
            subjects.extend(db.query(Subject).filter(Subject.standard_id == standard.id).all())

        # Retrieve modules
        modules = []
        for subject in subjects:
            modules.extend(db.query(Module).filter(Module.subject_id == subject.id).all())

        # Construct CourseCreateWithHierarchy object
        course_hierarchy = CourseCreateWithHierarchy(
            course={
                "name": course.name,
                "description": course.description
            },
            standards=[{
                "name": standard.name,
                "course_id": standard.course_id
            } for standard in standards],
            subjects=[{
                "name": subject.name,
                "standard_id": subject.standard_id
            } for subject in subjects],
            modules=[{
                "name": module.name,
                "subject_id": module.subject_id
            } for module in modules]
        )

        return course_hierarchy

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve course hierarchy: {str(e)}")

@router.get("/courses_hierarchy", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def get_all_courses_hierarchy(db: Session = Depends(get_db)):
    try:
        courses = db.query(Course).all()
        all_courses_hierarchy = []
        for course in courses:
            course_hierarchy = get_course_hierarchy(course.id, db)
            all_courses_hierarchy.append(course_hierarchy)
        return all_courses_hierarchy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve all courses hierarchy: {str(e)}")

@router.delete("/courses_delete/{course_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def delete_course_with_hierarchy(course_id: int, db: Session = Depends(get_db)):
    try:
        # Get the course
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Get the content paths associated with the course
        content_paths = db.query(Content.content_path).filter(Content.lesson_id == course_id).all()
        content_paths = [path for path, in content_paths]

        # Delete modules
        db.query(Module).filter(Module.subject_id.in_(db.query(Subject.id).filter(Subject.standard_id.in_(db.query(Standard.id)
                .filter(Standard.course_id == course_id))))).delete(synchronize_session=False)

        # Delete subjects
        db.query(Subject).filter(Subject.standard_id.in_(db.query(Standard.id).filter(Standard.course_id == course_id))).delete(synchronize_session=False)

        # Delete standards
        db.query(Standard).filter(Standard.course_id == course_id).delete(synchronize_session=False)

        # Delete course
        db.delete(course)
        db.commit()

        # Remove associated content files from storage
        for path in content_paths:
            if os.path.exists(path):
                os.remove(path)

        return {"message": "Course hierarchy deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete course hierarchy: {str(e)}")

    
##############################################################################################################################
@router.post("/courses/", response_model=None,
             dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        db_course = Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create course")


from sqlalchemy import distinct


@router.get("/courses/", response_model=None)
def read_all_courses(db: Session = Depends(get_db)):
    try:
        # Query distinct course names
        unique_course_names = db.query(Course.name).distinct().all()
        # Convert to a list
        unique_names = [name[0] for name in unique_course_names]
        return {"unique_courses": unique_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch courses")




@router.get("/courses/{course_id}", response_model=None)
def read_course(course_id: int, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return db_course
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch course")


@router.put("/courses/{course_id}", response_model=None,
            dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        db_course.name = course.name
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update course")


@router.delete("/courses/{course_id}", response_model=None,
               dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        db.delete(db_course)
        db.commit()
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete course")
    

