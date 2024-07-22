from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import json
import os
from ..models.Teacher import Teacher
from ..models import Lesson
from typing import List, Optional
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Content, Module
from ..schemas import ContentCreate
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
from pydantic import BaseModel
from sqlalchemy.orm import joinedload 
from ..models. courses_content import Course_content
import os
from dotenv import load_dotenv
from ..models import Course, TeacherCourse
from sqlalchemy import and_


load_dotenv()

router = APIRouter()

############################ post only content in content table #########################

@router.post("/content/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def create_content(
    name: str = Form(...),
    description: str = Form(None),
    content_type: str = Form(None),
    lesson_id: int = Form(...),
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    try:
        lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        file_paths = []

        for upload_file in files:
            unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
            file_path = os.path.join("static", "uploads", unique_filename)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            file_path = file_path.replace("\\", "/")
            
            file_paths.append(file_path)
        
        db_content = Content(
            name=name,
            description=description,
            content_type=content_type,
            lesson_id=lesson_id,
            content_path=file_paths
        )

        db.add(db_content)
        db.commit()
        db.refresh(db_content)

        return {"file_paths": file_paths}  # Returning the list of file paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=" failed to insert content")

############################ post  content and lession in content and lession table #########################
class ContentResponse(BaseModel):
    id: int
    name: str
    description: str
    content_path: List[str]

    class Config:
        from_attributes = True

class LessonResponse(BaseModel):
    lesson_id: int
    title: str
    contents: List[ContentResponse]

    class Config:
        from_attributes = True

@router.post("/content/with_lesson", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def create_lesson_and_content(
    course_content_id: int = Form(...),
    lesson_title: str = Form(...),
    content_descriptions: str = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    # Check if the course content exists and is associated with an assigned course
    course_content = db.query(Course_content).join(
        Course,
        Course.id == Course_content.course_id
    ).join(
        TeacherCourse,
        and_(
            TeacherCourse.course_id == Course.id,
            TeacherCourse.is_assign_course == True
        )
    ).filter(Course_content.id == course_content_id).first()

    if not course_content:
        raise HTTPException(status_code=404, detail="No assigned course content found for the given ID")

    # Create new lesson
    new_lesson = Lesson(
        title=lesson_title,
        course_content_id=course_content.id
    )
    db.add(new_lesson)
    db.flush()

    file_paths = []
    for upload_file in files:
        unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
        file_path = os.path.join("static", "uploads", unique_filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        file_path = file_path.replace("\\", "/")
        file_paths.append(file_path)

    new_content = Content(
        content_description=content_descriptions,
        content_path=file_paths,  
        lesson_id=new_lesson.lesson_id,
        course_content_id=course_content.id  
    )
    db.add(new_content)

    db.commit()
    return {"message": "Lesson and content created successfully"}

############################### get lession and content baase on course_content_id from course_content table  #######################


def get_lessons_by_course_content(db: Session, course_content_id: int):
    return db.query(Content).options(joinedload(Content.lesson)).filter(Content.course_content_id == course_content_id).all()

@router.get("/content", response_model=None)
async def get_lessons_and_content_based_on_content_id(
    course_content_id: int,
    db: Session = Depends(get_db)
):
    # Check if the course content exists
    course_content = db.query(Course_content).filter(Course_content.id == course_content_id).first()
    if not course_content:
        raise HTTPException(status_code=404, detail="Course content not found")
    
    contents = get_lessons_by_course_content(db, course_content_id)
    if not contents:
        raise HTTPException(status_code=404, detail="No lessons found for this course content")
    
    base_url_path = os.getenv("BASE_URL_PATH")  # Your base URL path
    result = []
    
    for content in contents:
        
        lesson_data = {
            "lesson_id": content.lesson.lesson_id,  
            "title": content.lesson.title,  
            #"description": content.lesson.description,  
            "course_content_id": content.lesson.course_content_id,
            "content_info": {  
                "id": content.id,
                #"name": content.name,
                "description": content.content_description,
                #"content_type": content.course_content_type,
                "content_path": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
            }
        }
        
        result.append(lesson_data)
    
    return result

########################################


    
@router.get("/content/get_all", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_all_content(db: Session = Depends(get_db)):
    try:
        contents = db.query(Content).all()
        if not contents:
            raise HTTPException(status_code=404, detail="No content found")
        
        base_url_path = os.getenv("BASE_URL_PATH")  # Your base URL path

        all_content_data = []
        for content in contents:
            content_data = {
                "id": content.id,
                #"name": content.name,
                "description": content.content_description,
                #"content_type": content.content_type,
                "lesson_id": content.lesson_id,
                "content_paths": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
            }
            all_content_data.append(content_data)

        return JSONResponse(content=all_content_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to fetch content")

@router.get("/content/{content_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        base_url_path = os.getenv("BASE_URL_PATH")  # Your base URL path

        content_data = {
            "id": content.id,
            #"name": content.name,
            "description": content.content_description,
            #"content_type": content.content_type,
            "lesson_id": content.lesson_id,
            "content_paths": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
        }

        return content_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to fetch content")

def increment_content_file_count(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if teacher:
        teacher.content_file_count += 1
        db.commit()

def decrement_content_file_count(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.Teacher_id == teacher_id).first()
    if teacher:
        if teacher.content_file_count > 0:
            teacher.content_file_count -= 1
            db.commit()

def delete_file_from_storage(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted successfully: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

from ..models.content import save_upload

def save_upload(files: List[UploadFile]) -> List[str]:
    file_paths = []
    try:
        for upload_file in files:
            unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
            file_path = os.path.join("static", "uploads", unique_filename)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            # Convert backslashes to forward slashes
            file_path = file_path.replace("\\", "/")
            file_paths.append(file_path)
        return file_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.put("/content/{content_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def update_content(
    content_id: int,
    name: str = Form(None),
    description: str = Form(None),
    content_type: str = Form(None),
    lesson_id: int = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if not db_content:
            raise HTTPException(status_code=404, detail="Content not found")

        original_content_path_count = len(db_content.content_path)
        original_content_paths = db_content.content_path[:]

        # Update name and description if provided
        if name is not None:
            db_content.name = name
        if description is not None:
            db_content.description = description

        # Update content_type if provided
        if content_type is not None:
            db_content.content_type = content_type

        # Update lesson_id
        db_content.lesson_id = lesson_id

        # Process uploaded files if provided
        if files:
            content_path_list = save_upload(files)
            db_content.content_path = content_path_list

        new_content_path_count = len(db_content.content_path)

        # Check if the number of files has changed
        if new_content_path_count > original_content_path_count:
            increment_content_file_count(db, db_content.id)
        elif new_content_path_count < original_content_path_count:
            # Delete excess files from storage
            excess_files = original_content_paths[new_content_path_count:]
            for file_path in excess_files:
                delete_file_from_storage(file_path)
            db_content.content_path = db_content.content_path[:new_content_path_count]

        db.commit()
        return {"message": "Content updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to update content")


    

@router.delete("/content/{content_id}", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
def delete_content(content_id: int, db: Session = Depends(get_db)):
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        db.delete(content)
        db.commit()

        if content.content_path:
            for file_path in content.content_path:
                if os.path.exists(file_path):
                    os.remove(file_path)

        return {"message": "Content deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to delete content")
    
# Get all contents
# @router.get("/contents/", response_model=None)
# async def read_contents(db: Session = Depends(get_db)):
#     return db.query(Content).all()

# # Get a specific content by ID
# @router.get("/contents/{content_id}", response_model=None)
# async def read_content(content_id: int, db: Session = Depends(get_db)):
#     content = db.query(Content).filter(Content.id == content_id).first()
#     if content is None:
#         raise HTTPException(status_code=404, detail="content not found")
#     return content

# # Create a new content
# @router.post("/contents/", response_model=None)
# async def create_content(content_data: ContentCreate, db: Session = Depends(get_db)):
#     content = Content(**content_data.dict())
#     db.add(content)
#     db.commit()
#     db.refresh(content)
#     return content

# # Update a content by ID
# @router.put("/contents/{content_id}", response_model=None)
# async def update_content(content_id: int, content_data: ContentUpdate, db: Session = Depends(get_db)):
#     content = db.query(Content).filter(Content.id == content_id).first()
#     if content is None:
#         raise HTTPException(status_code=404, detail="content not found")
#     for key, value in content_data.dict().items():
#         setattr(content, key, value)
#     db.commit()
#     db.refresh(content)
#     return content

# # Delete a content by ID
# @router.delete("/contents/{content_id}", response_model=None)
# async def delete_content(content_id: int, db: Session = Depends(get_db)):
#     content = db.query(Content).filter(Content.id == content_id).first()
#     if content is None:
#         raise HTTPException(status_code=404, detail="Content not found")
#     db.delete(content)
#     db.commit()
#     return content
