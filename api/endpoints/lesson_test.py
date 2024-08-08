from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from pydantic import BaseModel, Field
from ..schemas import QuestionCreate, QuestionGetResponse
from ..models import LmsUsers 
from typing import List, Optional
from fastapi import Form
import shutil
import uuid
import os
from auth.auth_bearer import JWTBearer,get_admin, get_teacher, get_admin_or_teacher
from .lms_users import router as lms_router, get_current_user
from sqlalchemy.exc import IntegrityError
import difflib
from ..models.lesson_student_test_ans import StudentAnswer
from ..models import QuestionPaper1,Lesson
from ..models import LessontestQuestion
import difflib
from PIL import Image
import numpy as np
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Question
# ------------------------------------------------------------------------------------------------------------------


def save_upload(upload_file: Optional[UploadFile]) -> Optional[str]:
    if not upload_file:
        return None
    
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

@router.post("/lesson-test-questions/", response_model=None)
async def create_question(
    question_paper_id: int = Form(None),
    question_text: str = Form(None),
    question_images: UploadFile = File(None),
    option1_text: str = Form(None),
    option1_images: UploadFile = File(None),
    option2_text: str = Form(None),
    option2_images: UploadFile = File(None),
    option3_text: str = Form(None),
    option3_images: UploadFile = File(None),
    option4_text: str = Form(None),
    option4_images: UploadFile = File(None),
    correct_ans_text: str = Form(None),
    correct_ans_images: UploadFile = File(None),
    difficulty_level: str = Form(None),
    per_question_marks: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        question_paper = db.query(QuestionPaper1).filter(QuestionPaper1.id == question_paper_id).first()
        if not question_paper:
            raise HTTPException(status_code=404, detail=f"Question paper with id {question_paper_id} not found")

        lesson = db.query(Lesson).filter(Lesson.lesson_id == question_paper.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson with id {question_paper.lesson_id} not found")

        db_question = LessontestQuestion(
            question_paper_id=question_paper_id,
            question_text=question_text,
            question_images=save_upload(question_images),
            option1_text=option1_text,
            option1_images=save_upload(option1_images),
            option2_text=option2_text,
            option2_images=save_upload(option2_images),
            option3_text=option3_text,
            option3_images=save_upload(option3_images),
            option4_text=option4_text,
            option4_images=save_upload(option4_images),
            correct_ans_text=correct_ans_text,
            correct_ans_images=save_upload(correct_ans_images),
            difficulty_level=difficulty_level,
            per_question_marks=per_question_marks
        )

        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        return {"message": "Question created successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()  
        print(f"Detailed error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
   
base_url_path = os.getenv("BASE_URL_PATH")

def prepend_base_url(path: Optional[str]) -> Optional[str]:
    if path:
        return f"{base_url_path}/{path}"
    return None

@router.post("/lesson-test-questions/student-answers/{question_id}/answer")
async def answer_question(
    question_id: int,
    user_answer: str = Form(...),  
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    student_answer = db.query(StudentAnswer).filter(
        StudentAnswer.user_id == current_user.user_id,
        StudentAnswer.question_paper_id == question.question_paper_id
    ).first()
    
    if not student_answer:
        student_answer = StudentAnswer(
            user_id=current_user.user_id,
            question_paper_id=question.question_paper_id,
            total_questions=0,
            correct_answer=0,
            wrong_answer=0,
            score=0,
            passed=False
        )
        db.add(student_answer)
        db.commit()
        db.refresh(student_answer)

    try:
        def get_option_number(answer):
            options = {
                (question.option1_text or "").lower().strip(): "option1",
                (question.option1_images or "").lower().strip(): "option1",
                (question.option2_text or "").lower().strip(): "option2",
                (question.option2_images or "").lower().strip(): "option2",
                (question.option3_text or "").lower().strip(): "option3",
                (question.option3_images or "").lower().strip(): "option3",
                (question.option4_text or "").lower().strip(): "option4",
                (question.option4_images or "").lower().strip(): "option4",
            }
            return options.get(answer.lower().strip())

        user_option = get_option_number(user_answer)

        if not user_option:
            raise HTTPException(status_code=400, detail="Invalid answer")

        is_correct = user_option == question.correct_ans_text

        student_answer.total_questions += 1
        student_answer.given_ans_text = user_option  
        student_answer.is_correct = is_correct
        if is_correct:
            student_answer.correct_answer += 1
        else:
            student_answer.wrong_answer += 1

       # Calculate score
        correct_points = student_answer.correct_answer * question.per_question_marks  
        # wrong_points = student_answer.wrong_answer * 0.25  
        # total_points = correct_points - wrong_points
        #max_possible_points = student_answer.total_questions*2 
        # student_answer.score = (total_points / max_possible_points) * 100 if max_possible_points > 0 else 0
        student_answer.score = correct_points

        # Ensure score is between 0 and 100
        #student_answer.score = max(min(student_answer.score, 100), 0)
        student_answer.passed = student_answer.score >= 40
        
        db.commit()
        db.refresh(student_answer)

        return {
            "student_id": current_user.user_id,
            "question_id": question_id,
            "question_text": question.question_text,
            "question_images": prepend_base_url(question.question_images),
            "options": {
                "option1_text": question.option1_text,
                "option1_images": prepend_base_url(question.option1_images),
                "option2_text": question.option2_text,
                "option2_images": prepend_base_url(question.option2_images),
                "option3_text": question.option3_text,
                "option3_images": prepend_base_url(question.option3_images),
                "option4_text": question.option4_text,
                "option4_images": prepend_base_url(question.option4_images),
            },
            "correct_ans": question.correct_ans_text,
            "user_answer": user_answer,
            "user_answer_image": student_answer.given_ans_image,
            "user_selected_option": user_option,  
            "is_correct": is_correct,
            "obtain_marks": student_answer.score,
            "total_questions_answered": student_answer.total_questions,
            "correct_answers": student_answer.correct_answer,
            "wrong_answers": student_answer.wrong_answer,
            "passed": student_answer.passed 
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the student answer")

@router.get("/lesson-test-questions/{question_id}", response_model=None)
async def get_lesson_test_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()
        
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        
        response_data = {
            "id": question.id,
            "question_paper_id": question.question_paper_id,
            "question_text": question.question_text,
            "question_image": prepend_base_url(question.question_images),
            "option1_text": question.option1_text,
            "option1_image": prepend_base_url(question.option1_images),
            "option2_text": question.option2_text,
            "option2_image": prepend_base_url(question.option2_images),
            "option3_text": question.option3_text,
            "option3_image": prepend_base_url(question.option3_images),
            "option4_text": question.option4_text,
            "option4_image": prepend_base_url(question.option4_images),
            "difficulty_level": question.difficulty_level,
            "per_question_marks": question.per_question_marks
        }
        
        if current_user.user_type in ["admin", "teacher"]:
            response_data["correct_answer_text"] = question.correct_ans_text
            response_data["correct_answer_image"] = prepend_base_url(question.correct_ans_images)
        
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")

@router.put("/questions/{question_id}", response_model=None)
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
    difficulty_level: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        db_question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()

        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        if question_text:
            db_question.question_text = question_text
        if option1_text:
            db_question.option1_text = option1_text
        if option2_text:
            db_question.option2_text = option2_text
        if option3_text:
            db_question.option3_text = option3_text
        if option4_text:
            db_question.option4_text = option4_text
        if correct_answer_text:
            db_question.correct_ans_text = correct_answer_text
        if difficulty_level:
            db_question.difficulty_level = difficulty_level

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
        

        # Commit the changes
        db.add(db_question)
        db.commit()

        return {"message": "Question has been updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()

        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        db.delete(db_question)
        db.commit()

        return {"message": "Question has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
