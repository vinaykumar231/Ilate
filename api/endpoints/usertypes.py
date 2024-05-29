from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from ..models import UserType
from ..schemas import UserTypeCreate, UserTypeUpdate

router = APIRouter()

# Get all user types
@router.get("/usertypes/", response_model=None)
async def read_usertypes(db: Session = Depends(get_db)):
    return db.query(UserType).all()

# Get a specific user type by ID
@router.get("/usertypes/{usertype_id}", response_model=None)
async def read_usertype(usertype_id: int, db: Session = Depends(get_db)):
    usertype = db.query(UserType).filter(UserType.id == usertype_id).first()
    if usertype is None:
        raise HTTPException(status_code=404, detail="User type not found")
    return usertype

# Create a new user type 
@router.post("/usertypes/", response_model=None)
async def create_usertype(usertype_data: UserTypeCreate, db: Session = Depends(get_db)):
    usertype = UserType(**usertype_data.dict())
    db.add(usertype)
    db.commit()
    db.refresh(usertype)
    return usertype

# Update a user type by ID
@router.put("/usertypes/{usertype_id}", response_model=None)
async def update_usertype(usertype_id: int, usertype_data: UserTypeUpdate, db: Session = Depends(get_db)):
    usertype = db.query(UserType).filter(UserType.id == usertype_id).first()
    if usertype is None:
        raise HTTPException(status_code=404, detail="User type not found")
    for key, value in usertype_data.dict().items():
        setattr(usertype, key, value)
    db.commit()
    db.refresh(usertype)
    return usertype

# Delete a user type by ID
@router.delete("/usertypes/{usertype_id}", response_model=None)
async def delete_usertype(usertype_id: int, db: Session = Depends(get_db)):
    usertype = db.query(UserType).filter(UserType.id == usertype_id).first()
    if usertype is None:
        raise HTTPException(status_code=404, detail="User type not found")
    db.delete(usertype)
    db.commit()
    return usertype
