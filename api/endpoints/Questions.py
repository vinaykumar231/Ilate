from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.Questions import Question as QuestionModel
from ..models.Questions import Question
from pydantic import BaseModel, Field
from ..schemas import QuestionCreate, QuestionGetResponse
from ..models.Questions import Question, save_upload
from ..models import LmsUsers 
from typing import List, Optional
from fastapi import Form
import shutil
import uuid
import os
from auth.auth_bearer import JWTBearer,get_admin, get_teacher, get_admin_or_teacher
from ..endpoints.lms_users import router as lms_router, get_current_user




router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Question
# ------------------------------------------------------------------------------------------------------------------

# Create Question endpoint
@router.post("/questions/", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def create_question(
    question_text: str = Form(None),
    question_image: UploadFile = File(default=None),
    option1_text: str = Form(None),
    option1_image: UploadFile = File(default=None),
    option2_text: str = Form(None),
    option2_image: UploadFile = File(default=None),
    option3_text: str = Form(None),
    option3_image: UploadFile = File(default=None),
    option4_text: str = Form(None),
    option4_image: UploadFile = File(default=None),
    correct_answer_text: str = Form(None),
    correct_answer_image: UploadFile = File(default=None),
    given_answer_text: str = Form(None),
    given_answer_image: UploadFile = File(default=None),
    difficulty_level: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Save all uploaded files and append their paths to a list
        file_paths = []
        for file in [question_image, option1_image, option2_image, option3_image, option4_image,
                     correct_answer_image, given_answer_image]:
            if file:
                file_path = f"static/uploads/{file.filename}"
                with open(file_path, "wb") as buffer:
                    buffer.write(file.file.read())
                file_paths.append(file_path)

        # Create Question instance
        db_question = Question(
            question_text=question_text,
            question_images=file_paths[0] if file_paths else None,
            option1_text=option1_text,
            option1_images=file_paths[1] if len(file_paths) > 1 else None,
            option2_text=option2_text,
            option2_images=file_paths[2] if len(file_paths) > 2 else None,
            option3_text=option3_text,
            option3_images=file_paths[3] if len(file_paths) > 3 else None,
            option4_text=option4_text,
            option4_images=file_paths[4] if len(file_paths) > 4 else None,
            given_ans_text=given_answer_text,
            given_ans_image=file_paths[5] if len(file_paths) > 5 else None,
            correct_ans_text=correct_answer_text,
            correct_ans_images=file_paths[6] if len(file_paths) > 6 else None,
            difficulty_level=difficulty_level
        )

        # Add to session and commit
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        return {"message": "Question has been created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")

# Get Question by ID
base_url_path = "http://192.168.29.40:8000"

@router.get("/questions/{question_id}", response_model=None)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        # Retrieve question from the database using the provided question_id
        db_question = db.query(Question).filter(Question.question_id == question_id).first()
        
        # Check if the question exists
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Prepare the response data
        response_data = {
            "question_id": db_question.question_id,
            "question_text": db_question.question_text,
            "question_image": prepend_base_url(db_question.question_images),
            "option1_text": db_question.option1_text,
            "option1_image": prepend_base_url(db_question.option1_images),
            "option2_text": db_question.option2_text,
            "option2_image": prepend_base_url(db_question.option2_images),
            "option3_text": db_question.option3_text,
            "option3_image": prepend_base_url(db_question.option3_images),
            "option4_text": db_question.option4_text,
            "option4_image": prepend_base_url(db_question.option4_images),
            "difficulty_level": db_question.difficulty_level,
        }
        
        # Add fields based on user type
        if current_user.user_type in ["admin", "teacher"]:
            response_data["correct_answer_text"] = db_question.correct_ans_text
            response_data["correct_answer_image"] = prepend_base_url(db_question.correct_ans_images)
            response_data["given_answer_text"] = db_question.given_ans_text
            response_data["given_answer_image"] = prepend_base_url(db_question.given_ans_image)
        
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")

def prepend_base_url(image_path):
    if image_path:
        return f"{base_url_path}/{image_path}"
    else:
        return None
    
@router.get("/questions/", response_model=None)
async def get_questions_by_range(
    start_id: int = Query(..., description="Start of the range for question IDs"),
    end_id: int = Query(..., description="End of the range for question IDs"),
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        # Retrieve questions from the database within the specified range
        db_questions = db.query(Question).filter(Question.question_id >= start_id, Question.question_id <= end_id).all()

        # Check if any questions exist within the specified range
        if not db_questions:
            raise HTTPException(status_code=404, detail="No questions found within the specified range")

        # Prepare the response data for each question
        response_data = []
        for db_question in db_questions:
            question_data = {
                "question_id": db_question.question_id,
                "question_text": db_question.question_text,
                "question_image": db_question.question_images,
                "options1_text": db_question.option1_text,
                "options1_image": db_question.option1_images,
                "options2_text": db_question.option2_text,
                "options2_image": db_question.option2_images,
                "options3_text": db_question.option3_text,
                "options3_image": db_question.option3_images,
                "options4_text": db_question.option4_text,
                "options4_image": db_question.option4_images,
                "difficulty_level": db_question.difficulty_level
            }

            # Add fields based on user type
            if current_user.user_type in ["admin", "teacher"]:
                question_data["correct_answer_text"] = db_question.correct_ans_text
                question_data["correct_answer_image"] = db_question.correct_ans_images
                question_data["given_answer_text"] = db_question.given_ans_text
                question_data["given_answer_image"] = db_question.given_ans_image
            
            response_data.append(question_data)
        
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")


# Update Question
# Update Question
@router.put("/questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def update_question(
    question_id: int,
    question_text: str = Form(None),
    question_image: UploadFile = File(default=None),
    option1_text: str = Form(None),
    option1_image: UploadFile = File(default=None),
    option2_text: str = Form(None),
    option2_image: UploadFile = File(default=None),
    option3_text: str = Form(None),
    option3_image: UploadFile = File(default=None),
    option4_text: str = Form(None),
    option4_image: UploadFile = File(default=None),
    correct_answer_text: str = Form(None),
    correct_answer_image: UploadFile = File(default=None),
    given_answer_text: str = Form(None),  # Added form field for given answer text
    given_answer_image: UploadFile = File(default=None),  # Added form field for given answer image
    difficulty_level: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Retrieve the question from the database
        db_question = db.query(Question).filter(Question.question_id == question_id).first()

        # Check if the question exists
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Update the question text and difficulty level if provided
        if question_text:
            db_question.question_text = question_text
        if difficulty_level:
            db_question.difficulty_level = difficulty_level

        # Update image data if provided
        if question_image:
            question_image_path = save_upload(question_image)
            db_question.question_images = question_image_path
        if option1_image:
            option1_image_path = save_upload(option1_image)
            db_question.option1_images = option1_image_path
        if option2_image:
            option2_image_path = save_upload(option2_image)
            db_question.option2_images = option2_image_path
        if option3_image:
            option3_image_path = save_upload(option3_image)
            db_question.option3_images = option3_image_path
        if option4_image:
            option4_image_path = save_upload(option4_image)
            db_question.option4_images = option4_image_path
        if correct_answer_image:
            correct_answer_image_path = save_upload(correct_answer_image)
            db_question.correct_ans_images = correct_answer_image_path
        
        # Update given answer data if provided
        if given_answer_text:
            db_question.given_ans_text = given_answer_text
        if given_answer_image:
            given_answer_image_path = save_upload(given_answer_image)
            db_question.given_ans_image = given_answer_image_path

        # Commit the changes
        db.commit()

        return {"message": "Question has been updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update question: {str(e)}")


# Delete Question
@router.delete("/questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Retrieve the question from the database
        db_question = db.query(Question).filter(Question.question_id == question_id).first()

        # Check if the question exists
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Delete the question from the database
        db.delete(db_question)
        db.commit()

        return {"message": "Question has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete question: {str(e)}")
