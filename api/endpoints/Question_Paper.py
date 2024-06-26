from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.Question_Paper import QuestionMapping as QuestionMappingModel
from pydantic import BaseModel, Field
from ..schemas import QuestionMappingCreate, QuestionMappingResponse




router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #Question  paper with mapping ID
# ------------------------------------------------------------------------------------------------------------------
    
# Create QuestionMapping
@router.post("/question_mappings/", response_model=QuestionMappingResponse)
def create_question_mapping(mapping: QuestionMappingCreate, db: Session = Depends(get_db)):
    try:
        db_mapping = QuestionMappingModel(**mapping.dict())
        db.add(db_mapping)
        db.commit()
        db.refresh(db_mapping)
        return db_mapping
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create question and paper with  mapping_id")
    
# Get QuestionMapping by ID
@router.get("/question_mappings/{mapping_id}", response_model=QuestionMappingResponse)
def get_question_mapping(mapping_id: int, db: Session = Depends(get_db)):
    try:
        db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
        if db_mapping is None:
            raise HTTPException(status_code=404, detail="QuestionMapping not found")
        return db_mapping
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question and paper with  mapping_id: {str(e)}")

# Update QuestionMapping
@router.put("/question_mappings/{mapping_id}", response_model=QuestionMappingResponse)
def update_question_mapping(mapping_id: int, mapping: QuestionMappingCreate, db: Session = Depends(get_db)):
    try:
        db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
        if db_mapping is None:
            raise HTTPException(status_code=404, detail="QuestionMapping not found")
        for key, value in mapping.dict().items():
            setattr(db_mapping, key, value)
        db.commit()
        db.refresh(db_mapping)
        return db_mapping
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update question and paper with  mapping_id: {str(e)}")

# Delete QuestionMapping
@router.delete("/question_mappings/{mapping_id}")
def delete_question_mapping(mapping_id: int, db: Session = Depends(get_db)):
    try:
        db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
        if db_mapping is None:
            raise HTTPException(status_code=404, detail="QuestionMapping not found")
        db.delete(db_mapping)
        db.commit()
        return {"message": "QuestionMapping deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete question and paper with  mapping_id: {str(e)}")

