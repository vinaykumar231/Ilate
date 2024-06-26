from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models.paper import Paper as PaperModel
from pydantic import BaseModel, Field
from ..schemas import PaperCreate, PaperResponse




router = APIRouter()

# ------------------------------------------------------------------------------------------------------------------
                        #paper  Table
# ------------------------------------------------------------------------------------------------------------------

# Create Paper
@router.post("/papers/", response_model=PaperResponse)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    try:
        db_paper = PaperModel(**paper.dict())
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        return db_paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert paper: {str(e)}")
# Get Paper by ID
@router.get("/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    try:
        db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
        if db_paper is None:
            raise HTTPException(status_code=404, detail="Paper not found")
        return db_paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch paper: {str(e)}")

# Update Paper
@router.put("/papers/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: int, paper: PaperCreate, db: Session = Depends(get_db)):
    try:
        db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
        if db_paper is None:
            raise HTTPException(status_code=404, detail="Paper not found")
        for key, value in paper.dict().items():
            setattr(db_paper, key, value)
        db.commit()
        db.refresh(db_paper)
        return db_paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update paper: {str(e)}")

# Delete Paper
@router.delete("/papers/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    try:
        db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
        if db_paper is None:
            raise HTTPException(status_code=404, detail="Paper not found")
        db.delete(db_paper)
        db.commit()
        return {"message": "Paper deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete paper: {str(e)}")
