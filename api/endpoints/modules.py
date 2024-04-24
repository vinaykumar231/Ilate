from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import Module
from ..schemas import ModuleCreate, ModuleUpdate

router = APIRouter()

# Get all modules
@router.get("/modules/", response_model=None)
async def read_modules(db: Session = Depends(get_db)):
    return db.query(Module).all()

# Get a specific module by ID
@router.get("/modules/{module_id}", response_model=None)
async def read_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

# Create a new module
@router.post("/modules/", response_model=None)
async def create_module(module_data: ModuleCreate, db: Session = Depends(get_db)):
    module = Module(**module_data.dict())
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

# Update a module by ID
@router.put("/modules/{module_id}", response_model=None)
async def update_module(module_id: int, module_data: ModuleUpdate, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    for key, value in module_data.dict().items():
        setattr(module, key, value)
    db.commit()
    db.refresh(module)
    return module

# Delete a module by ID
@router.delete("/modules/{module_id}", response_model=None)
async def delete_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    db.delete(module)
    db.commit()
    return module
