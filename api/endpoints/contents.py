from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
from ..models.Teacher import Teacher
from ..models import Lesson
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Content
from ..schemas import ContentCreate
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from auth.auth_bearer import JWTBearer, get_admin, get_teacher, get_admin_or_teacher
from fastapi.responses import JSONResponse
import os
import uuid
import shutil

router = APIRouter()

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
        
        # Create an empty list to store file paths
        file_paths = []

        # Iterate over uploaded files and process each one
        for upload_file in files:
            unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
            file_path = os.path.join("static", "uploads", unique_filename)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            # Convert backslashes to forward slashes
            file_path = file_path.replace("\\", "/")
            
            # Append the file path to the list
            file_paths.append(file_path)
        
        # Now you have the list of file paths, you can do whatever you need with it
        # For example, you can use it to create a new Content object
        
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
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/content/get_all", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_all_content(db: Session = Depends(get_db)):
    contents = db.query(Content).all()
    if not contents:
        raise HTTPException(status_code=404, detail="No content found")
    
    base_url_path = "http://192.168.29.82:8001"  # Your base URL path

    all_content_data = []
    for content in contents:
        content_data = {
            "id": content.id,
            "name": content.name,
            "description": content.description,
            "content_type": content.content_type,
            "lesson_id": content.lesson_id,
            "content_paths": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
        }
        all_content_data.append(content_data)

    return JSONResponse(content=all_content_data)

@router.get("/content/{content_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    base_url_path = "http://192.168.29.82:8001"  # Your base URL path

    content_data = {
        "id": content.id,
        "name": content.name,
        "description": content.description,
        "content_type": content.content_type,
        "lesson_id": content.lesson_id,
        "content_paths": [f"{base_url_path}/{path}" for path in content.content_path] if content.content_path else None
    }

    return content_data

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
        raise HTTPException(status_code=500, detail=str(e))


    

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
        raise HTTPException(status_code=500, detail=str(e))
    
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
