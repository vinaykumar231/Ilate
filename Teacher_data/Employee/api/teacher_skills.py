# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import SkillBase, SkillCreate,SkillUpdate
# from db.session import get_db
# from ..Model.teacher_skills import Skill
# from typing import List


# router = APIRouter()

# # Create skill record
# @router.post("/skills/", response_model=None)
# def create_skill( employee_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
#     db_skill = Skill( employee_id=employee_id, **skill.dict())
#     db.add(db_skill)
#     db.commit()
#     db.refresh(db_skill)
#     return db_skill


# # Read skill record by ID
# @router.get("/skills/{employee_id}", response_model=None)
# def read_skill(employee_id: int, db: Session = Depends(get_db)):
#     skill = db.query(Skill).filter(Skill.employee_id == employee_id).first()
#     if not skill:
#         raise HTTPException(status_code=404, detail="Skill not found")
#     return skill

# # Update skill record
# @router.put("/skills/{employee_id}", response_model=None)
# def update_skill(employee_id: int, skill_update: SkillUpdate, db: Session = Depends(get_db)):
#     db_skill = db.query(Skill).filter(Skill.employee_id == employee_id).first()
#     if not db_skill:
#         raise HTTPException(status_code=404, detail="Skill not found")
#     for key, value in skill_update.dict().items():
#         setattr(db_skill, key, value)
#     db.commit()
#     db.refresh(db_skill)
#     return db_skill

# # Delete skill record
# @router.delete("/skills/{employee_id}")
# def delete_skill(employee_id: int, db: Session = Depends(get_db)):
#     skill = db.query(Skill).filter(Skill.employee_id == employee_id).first()
#     if not skill:
#         raise HTTPException(status_code=404, detail="Skill not found")
#     db.delete(skill)
#     db.commit()
#     return {"message": "Skill deleted successfully"}