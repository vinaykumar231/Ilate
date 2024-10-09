from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Branch
from ..schemas import BranchCreate, BranchUpdate

router = APIRouter()

@router.post("/branches/", response_model=None)
async def create_branch(branch_data: BranchCreate, db: Session = Depends(get_db)):
    try:
        branch = Branch(**branch_data.dict())
        db.add(branch)
        db.commit()
        db.refresh(branch)
        return branch
    except Exception as e:
        raise HTTPException(status_code=500, detail=" failed to insert branch")

# @router.get("/branches/", response_model=None)
# async def read_all_branches(db: Session = Depends(get_db)):
#     try:
#         return db.query(Branch).all()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=" failed to fetch branch")
    
@router.get("/branches/get_all/", response_model=None)
async def read_all_branches(db: Session = Depends(get_db)):
    try:
        all_data=[]
        get_data=db.query(Branch).all()
        for branch in get_data:
            data={
                "id":branch.id,
                "name":branch.name,
            }
            all_data.append(data)
        return {"all_branches":all_data}
    except:
        raise HTTPException(status_code=404, detail="branch not found")
        
        

@router.get("/branches/{branch_id}", response_model=None)
async def read_branch(branch_id: int, db: Session = Depends(get_db)):
    try:
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if branch is None:
            raise HTTPException(status_code=404, detail="Branch not found")
        return branch
    except Exception as e:
        raise HTTPException(status_code=500, detail=" failed to fetch branch")

@router.put("/branches/{branch_id}", response_model=None)
async def update_branch(branch_id: int, branch_data: BranchUpdate, db: Session = Depends(get_db)):
    try:
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if branch is None:
            raise HTTPException(status_code=404, detail="Branch not found")
        for key, value in branch_data.dict().items():
            setattr(branch, key, value)
        db.commit()
        db.refresh(branch)
        return branch
    except Exception as e:
        raise HTTPException(status_code=500, detail=" failed to update branch")

@router.delete("/branches/{branch_id}", response_model=None)
async def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    try:
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if branch is None:
            raise HTTPException(status_code=404, detail="Branch not found")
        db.delete(branch)
        db.commit()
        return branch
    except Exception as e:
        raise HTTPException(status_code=500, detail=" failed to delete batch")
