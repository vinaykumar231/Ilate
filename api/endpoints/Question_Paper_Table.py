from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.Question_Paper_Table import QuestionPaper as  QuestionPaperModel
from pydantic import BaseModel, Field
from ..models import Teacher, Student, Subject, Module, Lesson, Test
from ..schemas import QuestionPaperCreate, QuestionPaperResponse



router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Question  paper Table
# ------------------------------------------------------------------------------------------------------------------

# QuestionPaper routes
@router.post("/question_papers/", response_model=None)
def create_question_paper(question_paper: QuestionPaperCreate, db: Session = Depends(get_db)):
    try:
        db_question_paper = QuestionPaperModel(**question_paper.dict())
        db.add(db_question_paper)
        db.commit()
        db.refresh(db_question_paper)
        return db_question_paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
     
# Get QuestionPaper by ID
@router.get("/question_papers/{question_paper_id}", response_model=None)
def get_question_paper(question_paper_id: int, db: Session = Depends(get_db)):
    db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
    if db_question_paper is None:
        raise HTTPException(status_code=404, detail="QuestionPaper not found")
    return db_question_paper

# Update QuestionPaper
from fastapi import HTTPException

@router.put("/question_papers/{question_paper_id}", response_model=None)
def update_question_paper(question_paper_id: int, question_paper: QuestionPaperCreate, db: Session = Depends(get_db)):
    try:
        db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
        if db_question_paper is None:
            raise HTTPException(status_code=404, detail="QuestionPaper not found")
        
        # Check if related entities exist and gather missing ones
        missing_entities = []
        if not db.query(Teacher).filter(Teacher.Teacher_id == question_paper.teacher_id).first():
            missing_entities.append("Teacher")
        if not db.query(Student).filter(Student.id == question_paper.student_id).first():
            missing_entities.append("Student")
        if not db.query(Subject).filter(Subject.id == question_paper.subject_id).first():
            missing_entities.append("Subject")
        if not db.query(Module).filter(Module.id == question_paper.module_id).first():
            missing_entities.append("Module")
        if not db.query(Lesson).filter(Lesson.lesson_id == question_paper.lesson_id).first():
            missing_entities.append("Lesson")
        if not db.query(Test).filter(Test.test_id == question_paper.test_id).first():
            missing_entities.append("Test")

        # Raise an exception if any entities are missing
        if missing_entities:
            raise HTTPException(status_code=404, detail=f"{', '.join(missing_entities)} not found")

        # Update question_paper attributes
        for key, value in question_paper.dict().items():
            setattr(db_question_paper, key, value)
        
        db.commit()
        db.refresh(db_question_paper)
        
        return {"message": "QuestionPaper updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete QuestionPaper
@router.delete("/question_papers/{question_paper_id}")
def delete_question_paper(question_paper_id: int, db: Session = Depends(get_db)):
    db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
    if db_question_paper is None:
        raise HTTPException(status_code=404, detail="QuestionPaper not found")
    db.delete(db_question_paper)
    db.commit()
    return {"message": "QuestionPaper deleted successfully"}
