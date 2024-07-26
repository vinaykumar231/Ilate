# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.session import get_db
# from ..models.Test import Test as TestModel
# from pydantic import BaseModel, Field
# from ..schemas import TestCreate, TestResponse




# router = APIRouter()

# # ------------------------------------------------------------------------------------------------------------------
#                         #Test
# # ------------------------------------------------------------------------------------------------------------------

# # Create Test
# @router.post("/tests/", response_model=None)
# async def create_test(test: TestCreate, db: Session = Depends(get_db)):
#     try:
#         # Create Test instance
#         db_test =TestModel(**test.dict())

#         # Add test to database
#         db.add(db_test)
#         db.commit()
#         db.refresh(db_test)

#         return db_test
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to create test: {str(e)}")
    
# @router.get("/tests/all_test", response_model=None)
# def get_all_tests(db: Session = Depends(get_db)):
#     try:
#         tests = db.query(TestModel).all()
#         return tests
#     except Exception as e:
#         raise HTTPException(status_code=404, detail="test not found")

# # Get Test by ID
# @router.get("/tests/{test_id}", response_model=None)
# def get_test(test_id: int, db: Session = Depends(get_db)):
#     try:
#         db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#         if db_test is None:
#             raise HTTPException(status_code=404, detail="Test not found")
#         return db_test
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Update Test
# @router.put("/tests/{test_id}", response_model=None)
# def update_test(test_id: int, test: TestCreate, db: Session = Depends(get_db)):
#     try:
#         db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#         if db_test is None:
#             raise HTTPException(status_code=404, detail="Test not found")
#         for key, value in test.dict().items():
#             setattr(db_test, key, value)
#         db.commit()
#         db.refresh(db_test)
#         return db_test
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to update test: {str(e)}")

# # Delete Test
# @router.delete("/tests/{test_id}")
# def delete_test(test_id: int, db: Session = Depends(get_db)):
#     try:
#         db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#         if db_test is None:
#             raise HTTPException(status_code=404, detail="Test not found")
#         db.delete(db_test)
#         db.commit()
#         return {"message": "Test deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to delete test: {str(e)}")

