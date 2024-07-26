from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
#from ..models.Questions import Question1 as QuestionModel
#from ..models.Questions import Question1
from pydantic import BaseModel, Field
from ..schemas import QuestionCreate, QuestionGetResponse
#from ..models.Questions import Question, save_upload
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
        
        # Convert backslashes to forward slashes
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
        # Check if the question_paper_id exists
        question_paper = db.query(QuestionPaper1).filter(QuestionPaper1.id == question_paper_id).first()
        if not question_paper:
            raise HTTPException(status_code=404, detail=f"Question paper with id {question_paper_id} not found")

        # Check if the associated lesson exists
        lesson = db.query(Lesson).filter(Lesson.lesson_id == question_paper.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson with id {question_paper.lesson_id} not found")

        # Create Question instance
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

        # Add to session and commit
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        return {"message": "Question created successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of error
        print(f"Detailed error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
   
def image_to_string(image_path):
    """Convert an image to a string representation."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        return img_array.tobytes().decode('latin-1')
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def is_answer_correct(selected_ans, selected_ans_image, correct_ans, correct_ans_image):
    similarity_threshold = 0.9

    # Text comparison
    if selected_ans and correct_ans:
        selected_ans = selected_ans.lower().strip()
        correct_ans = correct_ans.lower().strip()
        text_similarity = difflib.SequenceMatcher(None, selected_ans, correct_ans).ratio()
        if text_similarity >= similarity_threshold or selected_ans == correct_ans:
            return True

    # Image comparison
    if selected_ans_image and correct_ans_image:
        selected_img_str = image_to_string(selected_ans_image)
        correct_img_str = image_to_string(correct_ans_image)
        image_similarity = difflib.SequenceMatcher(None, selected_img_str, correct_img_str).ratio()
        if image_similarity >= similarity_threshold:
            return True

    return False

@router.post("/lesson-test-questions/student-answers/{question_id}/answer")
async def answer_question(
    question_id: int,
    selected_ans_text: Optional[str] = Form(None),
    selected_ans_image: UploadFile = File(None),
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
        # Initialize student_answer if no previous results
        student_answer = StudentAnswer(
            user_id=current_user.user_id,
            question_paper_id=question.question_paper_id,
            total_questions=0,
            wrong_answer=0,
            score=0,
            passed=False
        )
        db.add(student_answer)
        db.commit()
        db.refresh(student_answer)

    try:
       
        # Handle the image file if it's uploaded
        temp_image_path = None
        if selected_ans_image:
            temp_image_path = f"temp_{selected_ans_image.filename}"
            with open(temp_image_path, "wb") as buffer:
                buffer.write(await selected_ans_image.read())

        # Check if the answer is correct
        is_correct = is_answer_correct(
            selected_ans_text,
            question.correct_ans_text,
            temp_image_path,
            question.correct_ans_images
        )

        # Update student's answer statistics
        student_answer.total_questions += 1
        student_answer.given_ans_text = selected_ans_text
        student_answer.is_correct = is_correct
        if not is_correct:
            student_answer.wrong_answer += 1

        # Calculate score
        correct_answers = student_answer.total_questions - student_answer.wrong_answer
        student_answer.score = (correct_answers / student_answer.total_questions) * 100 if student_answer.total_questions > 0 else 0
        
        # Ensure score is between 0 and 100
        student_answer.score = max(min(student_answer.score, 100), 0)
        student_answer.passed = student_answer.score >= 75
        
        db.commit()
        db.refresh(student_answer)

        return {
            "student_id": current_user.user_id,
            "question_id": question_id,
            "question_text": question.question_text,
            "options": {
                "option1": question.option1_text,
                "option2": question.option2_text,
                "option3": question.option3_text,
                "option4": question.option4_text,
            },
            "correct_answer": question.correct_ans_text,
            "user_answer": selected_ans_text,
            "is_correct": is_correct,
            "score_in_%": student_answer.score,
            "total_questions_answered": student_answer.total_questions,
            "correct_answers": student_answer.total_questions - student_answer.wrong_answer,
            "wrong_answers": student_answer.wrong_answer,
            "passed": student_answer.passed 
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the student answer")
# Get Question by ID
base_url_path = "http://192.168.29.40:8000"

def prepend_base_url(path: Optional[str]) -> Optional[str]:
    if path:
        return f"{base_url_path}/{path}"
    return None

@router.get("/lesson-test-questions/{question_id}", response_model=None)
async def get_lesson_test_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        # Retrieve question from the database using the provided question_id
        question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()
        
        # Check if the question exists
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Prepare the response data
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
        
        # Add correct answer fields if the user is an admin or teacher
        if current_user.user_type in ["admin", "teacher"]:
            response_data["correct_answer_text"] = question.correct_ans_text
            response_data["correct_answer_image"] = prepend_base_url(question.correct_ans_images)
        
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")


# Update Question
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
        # Retrieve the question from the database
        db_question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()

        # Check if the question exists
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Update the question text and difficulty level if provided
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
        

        # Commit the changes
        db.add(db_question)
        db.commit()

        return {"message": "Question has been updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete Question
@router.delete("/questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Retrieve the question from the database
        db_question = db.query(LessontestQuestion).filter(LessontestQuestion.id == question_id).first()

        # Check if the question exists
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Delete the question from the database
        db.delete(db_question)
        db.commit()

        return {"message": "Question has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
