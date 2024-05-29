# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import ManagerCreate,ManagerUpdate
# from db.session import get_db
# from ..Model.manager import Manager
# from typing import List

# router = APIRouter()

# @router.post("/managers/", response_model=None)
# def create_manager(manager: ManagerCreate, db: Session = Depends(get_db)):
#     db_manager = Manager(**manager.dict())
#     db.add(db_manager)
#     db.commit()
#     db.refresh(db_manager)
#     return db_manager

# @router.get("/managers/{manager_id}", response_model=None)
# def get_manager(manager_id: int, db: Session = Depends(get_db)):
#     manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
#     if not manager:
#         raise HTTPException(status_code=404, detail="Manager not found")
#     return manager

# @router.put("/managers/{manager_id}", response_model=None)
# def update_manager(manager_id: int, manager_update: ManagerUpdate, db: Session = Depends(get_db)):
#     db_manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
#     if not db_manager:
#         raise HTTPException(status_code=404, detail="Manager not found")
#     for key, value in manager_update.dict().items():
#         setattr(db_manager, key, value)
#     db.commit()
#     db.refresh(db_manager)
#     return db_manager

# @router.delete("/managers/{manager_id}", response_model=None)
# def delete_manager(manager_id: int, db: Session = Depends(get_db)):
#     manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
#     if not manager:
#         raise HTTPException(status_code=404, detail="Manager not found")
#     db.delete(manager)
#     db.commit()
#     return "Manager deleted successfully" 