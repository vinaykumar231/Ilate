from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
#from ..models.Questions import Question as QuestionModel
from ..models.Discount_assesment_paper import DiscountQuestion
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
from ..endpoints.lms_users import router as lms_router, get_current_user
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
#from ..models.Discount_correct_ans import DiscountCorrectAnswer
from ..models.Discount_Ass_result import DiscountAssessmentResut
from pathlib import Path
import difflib


load_dotenv()
router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        # Discount Question paper
# ------------------------------------------------------------------------------------------------------------------

################### create question paper for admin #######################

@router.post("/Discount_questions/", response_model=None)
async def create_question(
    question_text: str = Form(None),
    option1_text: str = Form(None),
    option2_text: str = Form(None),
    option3_text: str = Form(None),
    option4_text: str = Form(None),
    correct_answer_text: str = Form(None),
    difficulty_level: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        
        # Create Question instance
        db_question = DiscountQuestion(
            question_text=question_text,
            option1_text=option1_text,
            option2_text=option2_text,
            option3_text=option3_text,
            option4_text=option4_text,
            correct_ans_text=correct_answer_text,
            difficulty_level=difficulty_level
        )
        
        # Add to session and commit
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        return db_question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
    
# Function to check the similarity of two answers
def is_answer_correct(selected_ans, correct_ans):
    # Convert both answers to lowercase for case-insensitive comparison
    selected_ans = selected_ans.lower()
    correct_ans = correct_ans.lower()
    similarity = difflib.SequenceMatcher(None, selected_ans, correct_ans).ratio()
    similarity_threshold = 0.9
    if similarity >= similarity_threshold or selected_ans == correct_ans:
        return True
    else:
        return False

#################### Route to handle answering a question #################

@router.post("/Discount_questions/{question_id}/answer")
async def answer_question(
    question_id: int,
    selected_ans_text: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    question = db.query(DiscountQuestion).filter(DiscountQuestion.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    user_overall_result = db.query(DiscountAssessmentResut).filter(
        DiscountAssessmentResut.user_id == current_user.user_id
    ).first()
    
    if not user_overall_result:
        # Initialize user_overall_result if no previous results
        user_overall_result = DiscountAssessmentResut(
            user_id=current_user.user_id,
            total_questions=0,
            correct_answers=0,
            wrong_answer=0,
            score=0,
            passed=False
        )
        db.add(user_overall_result)
        db.commit()
        db.refresh(user_overall_result)

    try:
        # Check if the answer is correct
        is_correct = is_answer_correct(selected_ans_text, question.correct_ans_text)

        # Update user's overall statistics
        user_overall_result.total_questions += 1
        if is_correct:
            user_overall_result.correct_answers += 1
        else:
            user_overall_result.wrong_answer += 1
        # Calculate score with negative marking
        obtain_marks = user_overall_result.correct_answers * 2  # 2 point for each correct answer
        # wrong_points = user_overall_result.wrong_answer * 0.25  # 0.25 point deduction for each wrong answer
        # total_points = correct_points - wrong_points
        total_marks = user_overall_result.total_questions*2 
        user_overall_result.score = (obtain_marks / total_marks) * 100 if total_marks > 0 else 0
        
        # Ensure score doesn't go below 0
        user_overall_result.score = max(user_overall_result.score, 0)
        user_overall_result.score = min(user_overall_result.score, 100)
        user_overall_result.passed = user_overall_result.score >= 75
        db.commit()
        db.refresh(user_overall_result)

        return {
            "user_id": current_user.user_id,
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
            "score_in_%": user_overall_result.score,
            "total_questions_answered": user_overall_result.total_questions,
            "correct_answers": user_overall_result.correct_answers,
            "wrong_answers": user_overall_result.wrong_answer,
            "passed": user_overall_result.passed 
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the assessment result")
########################################################################

base_url_path = os.getenv("BASE_URL_PATH")

def prepend_base_url(path: Optional[str]) -> Optional[str]:
    if path:
        return f"{base_url_path}/{path}"
    return None

@router.get("/Discount_questions/{question_id}", response_model=None)
async def get_lesson_test_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: LmsUsers = Depends(get_current_user)
):
    try:
        # Retrieve question from the database using the provided question_id
        question = db.query(DiscountQuestion).filter(DiscountQuestion.question_id == question_id).first()
        
        # Check if the question exists
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Prepare the response data
        response_data = {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "option1_text": question.option1_text,
            "option2_text": question.option2_text,
            "option3_text": question.option3_text,
            "option4_text": question.option4_text,
            "difficulty_level": question.difficulty_level,
            
        }
        
        # Add correct answer fields if the user is an admin or teacher
        if current_user.user_type in ["admin", "teacher"]:
            response_data["correct_answer_text"] = question.correct_ans_text
            
        
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")



# Update Question
# Update Question
@router.put("/Discount_questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def update_question(
    question_id: int,
    question_text: str = Form(None),
    option1_text: str = Form(None),
    option2_text: str = Form(None),
    option3_text: str = Form(None),
    option4_text: str = Form(None),
    correct_answer_text: str = Form(None),
    difficulty_level: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Retrieve the question from the database
        db_question = db.query(DiscountQuestion).filter(DiscountQuestion.question_id == question_id).first()

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

        # Commit the changes
        db.commit()

        return {"message": "Question has been updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update question: {str(e)}")


# Delete Question
@router.delete("/Discount_questions/{question_id}", response_model=None, dependencies=[Depends(JWTBearer()), Depends(get_admin_or_teacher)])
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_question = db.query(DiscountQuestion).filter(DiscountQuestion.question_id == question_id).first()
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        db.delete(db_question)
        db.commit()

        return {"message": "Question has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete question: {str(e)}")