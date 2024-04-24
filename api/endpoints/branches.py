from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Branch
from ..schemas import BranchCreate, BranchUpdate

router = APIRouter()

# Get all branches
@router.get("/branches/", response_model=None)
async def read_branches(db: Session = Depends(get_db)):
    return db.query(Branch).all()

# Get a specific branch by ID
@router.get("/branches/{branch_id}", response_model=None)
async def read_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

# Create a new branch
@router.post("/branches/", response_model=None)
async def create_branch(branch_data: BranchCreate, db: Session = Depends(get_db)):
    branch = Branch(**branch_data.dict())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

# Update a branch by ID
@router.put("/branches/{branch_id}", response_model=None)
async def update_branch(branch_id: int, branch_data: BranchUpdate, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    for key, value in branch_data.dict().items():
        setattr(branch, key, value)
    db.commit()
    db.refresh(branch)
    return branch

# Delete a branch by ID
@router.delete("/branches/{branch_id}", response_model=None)
async def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    db.delete(branch)
    db.commit()
    return branch
