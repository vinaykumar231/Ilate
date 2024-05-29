# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from ..scheemas import LanguagesSpokenBase, LanguagesSpokenCreate,LanguagesSpokenUpdate
# from db.session import get_db
# from ..Model.teacher_lang_knowledge import  LanguagesSpoken
# from typing import List


# router = APIRouter()

# # Create languages spoken record
# @router.post("/languages_spoken/", response_model=None)
# def create_languages_spoken(employee_id: int, languages_spoken: LanguagesSpokenCreate, db: Session = Depends(get_db)):
#     db_languages_spoken = LanguagesSpoken( employee_id=employee_id, **languages_spoken.dict())
#     db.add(db_languages_spoken)
#     db.commit()
#     db.refresh(db_languages_spoken)
#     return db_languages_spoken


# # Read languages spoken record by ID
# @router.get("/languages_spoken/{employee_id}", response_model=None)
# def read_languages_spoken_by_id(employee_id: int, db: Session = Depends(get_db)):
#     languages_spoken = db.query(LanguagesSpoken).filter(LanguagesSpoken.employee_id == employee_id).first()
#     if not languages_spoken:
#         raise HTTPException(status_code=404, detail="Languages spoken not found")
#     return languages_spoken

# # Update languages spoken record
# @router.put("/languages_spoken/{employee_id}", response_model=None)
# def update_languages_spoken(employee_id: int, languages_spoken_update: LanguagesSpokenUpdate, db: Session = Depends(get_db)):
#     db_languages_spoken = db.query(LanguagesSpoken).filter(LanguagesSpoken.employee_id == employee_id).first()
#     if not db_languages_spoken:
#         raise HTTPException(status_code=404, detail="Languages spoken not found")
#     for key, value in languages_spoken_update.dict().items():
#         setattr(db_languages_spoken, key, value)
#     db.commit()
#     db.refresh(db_languages_spoken)
#     return db_languages_spoken

# # Delete languages spoken record
# @router.delete("/languages_spoken/{employee_id}")
# def delete_languages_spoken(employee_id: int, db: Session = Depends(get_db)):
#     languages_spoken = db.query(LanguagesSpoken).filter(LanguagesSpoken.employee_id == employee_id).first()
#     if not languages_spoken:
#         raise HTTPException(status_code=404, detail="Languages spoken not found")
#     db.delete(languages_spoken)
#     db.commit()
#     return {"message": "Languages spoken deleted successfully"}
