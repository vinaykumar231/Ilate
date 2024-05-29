# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.session import SessionLocal, engine
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, Field
# from fastapi import APIRouter, Depends, HTTPException,UploadFile, File
# from sqlalchemy.orm import Session
# from ..models.proof import Image, save_image_to_db, get_image_by_user_id,update_image_in_db, delete_image_from_db
# from ..models.Question_Paper_Table import QuestionPaper as  QuestionPaperModel
# from ..models.Question_Paper import QuestionMapping as QuestionMappingModel
# from ..models.Teacher import Teacher as TeacherModel
# from ..models.course import Course as CourseModel
# from ..models.Students import Student as StudentModel
# from ..models.subject import Subject as SubjectModel
# from ..models.module import Module as ModuleModel
# from ..models.lession import Lesson as LessonModel
# from ..models.Questions import Question as QuestionModel
# from ..models.Question_Paper import QuestionMapping as QuestionMappingModel
# from ..models.Test import Test as TestModel
# from ..models.paper import Paper as PaperModel
# from db.session import get_db
# from typing import List, Optional
# from ..models.Questions import Question
# from fastapi import Form
# import shutil
# import uuid
# import os



# router = APIRouter()

# # ------------------------------------------------------------------------------------------------------------------
#                         #ID and Address proof
# # ------------------------------------------------------------------------------------------------------------------

# class ImageResponse(BaseModel):
#     user_id: int
#     id_prof:  Optional[str] = None
#     Address_prof:  Optional[str] = None

    
# @router.post("/proof", response_model=ImageResponse)
# async def upload_proof(
#     user_id: int,
#     id_prof: UploadFile = File(default=None),
#     Address_prof: UploadFile = File(default=None),
#     db: Session = Depends(get_db)
# ):
#     unique_id_prof_filename = None
#     unique_address_prof_filename = None

#     if id_prof:
#         unique_id_prof_filename = str(uuid.uuid4()) + "_" + id_prof.filename
#         id_prof_file_path = os.path.join("uploads", unique_id_prof_filename)
    
#     if Address_prof:
#         unique_address_prof_filename = str(uuid.uuid4()) + "_" + Address_prof.filename
#         Address_prof_file_path = os.path.join("uploads", unique_address_prof_filename)
    
#     try:
#         if id_prof:
#             with open(id_prof_file_path, "wb") as buffer:
#                 shutil.copyfileobj(id_prof.file, buffer)
        
#         if Address_prof:
#             with open(Address_prof_file_path, "wb") as buffer:
#                 shutil.copyfileobj(Address_prof.file, buffer)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
#     db_image = save_image_to_db(db, user_id, id_prof=unique_id_prof_filename, Address_prof=unique_address_prof_filename)
#     return db_image


# @router.get("/proof/{user_id}", response_model=ImageResponse)
# async def get_image(user_id: int, db: Session = Depends(get_db)):
#     db_image = get_image_by_user_id(user_id, db)
#     if db_image is None:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return ImageResponse(user_id=db_image.user_id, id_prof=db_image.id_prof, Address_prof=db_image.Address_prof)

# @router.put("/proof/{user_id}")
# async def update_image(
#     user_id: int,
#     id_prof: UploadFile = File(None),
#     Address_prof: UploadFile = File(None),
#     db: Session = Depends(get_db)
# ):
#     return update_image_in_db(db, user_id, id_prof, Address_prof)

# @router.delete("/proof/{user_id}")
# async def delete_image(user_id: int, db: Session = Depends(get_db)):
#     return delete_image_from_db(db, user_id)


# # ------------------------------------------------------------------------------------------------------------------
#                         #Question  paper Table
# # ------------------------------------------------------------------------------------------------------------------

# class QuestionPaperCreate(BaseModel):
#     title: str
#     description: str
#     teacher_id: int
#     students_id: int  
#     subject_id: int
#     module_id: int
#     lesson_id: int

# # Pydantic schema for QuestionPaper response
# class QuestionPaperResponse(BaseModel):
#     id: int
#     title: str
#     description: str
#     teacher_id: int
#     students_id: int
#     subject_id: int
#     module_id: int
#     lesson_id: int
    

# @router.post("/question_papers/", response_model=QuestionPaperResponse)
# def create_question_paper(question_paper: QuestionPaperCreate, db: Session = Depends(get_db)):
#     try:
#         db_question_paper = QuestionPaperModel(**question_paper.dict())
#         db.add(db_question_paper)
#         db.commit()
#         db.refresh(db_question_paper)
#         return db_question_paper
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# # Get QuestionPaper by ID
# @router.get("/question_papers/{question_paper_id}", response_model=QuestionPaperResponse)
# def get_question_paper(question_paper_id: int, db: Session = Depends(get_db)):
#     db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
#     if db_question_paper is None:
#         raise HTTPException(status_code=404, detail="QuestionPaper not found")
#     return db_question_paper

# # Update QuestionPaper
# @router.put("/question_papers/{question_paper_id}", response_model=QuestionPaperResponse)
# def update_question_paper(question_paper_id: int, question_paper: QuestionPaperCreate, db: Session = Depends(get_db)):
#     db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
#     if db_question_paper is None:
#         raise HTTPException(status_code=404, detail="QuestionPaper not found")
#     for key, value in question_paper.dict().items():
#         setattr(db_question_paper, key, value)
#     db.commit()
#     db.refresh(db_question_paper)
#     return db_question_paper

# # Delete QuestionPaper
# @router.delete("/question_papers/{question_paper_id}")
# def delete_question_paper(question_paper_id: int, db: Session = Depends(get_db)):
#     db_question_paper = db.query(QuestionPaperModel).filter(QuestionPaperModel.id == question_paper_id).first()
#     if db_question_paper is None:
#         raise HTTPException(status_code=404, detail="QuestionPaper not found")
#     db.delete(db_question_paper)
#     db.commit()
#     return {"message": "QuestionPaper deleted successfully"}

# # ------------------------------------------------------------------------------------------------------------------
#                         #Question  paper with mapping ID
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for QuestionMapping
# class QuestionMappingCreate(BaseModel):
#     paper_id: int
#     question_id: int

# class QuestionMappingResponse(BaseModel):
#     mapping_id: int
#     paper_id: int
#     question_id: int
    
# # Create QuestionMapping
# @router.post("/question_mappings/", response_model=QuestionMappingResponse)
# def create_question_mapping(mapping: QuestionMappingCreate, db: Session = Depends(get_db)):
#     try:
#         db_mapping = QuestionMappingModel(**mapping.dict())
#         db.add(db_mapping)
#         db.commit()
#         db.refresh(db_mapping)
#         return db_mapping
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to create question mapping")
    
# # Get QuestionMapping by ID
# @router.get("/question_mappings/{mapping_id}", response_model=QuestionMappingResponse)
# def get_question_mapping(mapping_id: int, db: Session = Depends(get_db)):
#     db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
#     if db_mapping is None:
#         raise HTTPException(status_code=404, detail="QuestionMapping not found")
#     return db_mapping

# # Update QuestionMapping
# @router.put("/question_mappings/{mapping_id}", response_model=QuestionMappingResponse)
# def update_question_mapping(mapping_id: int, mapping: QuestionMappingCreate, db: Session = Depends(get_db)):
#     db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
#     if db_mapping is None:
#         raise HTTPException(status_code=404, detail="QuestionMapping not found")
#     for key, value in mapping.dict().items():
#         setattr(db_mapping, key, value)
#     db.commit()
#     db.refresh(db_mapping)
#     return db_mapping

# # Delete QuestionMapping
# @router.delete("/question_mappings/{mapping_id}")
# def delete_question_mapping(mapping_id: int, db: Session = Depends(get_db)):
#     db_mapping = db.query(QuestionMappingModel).filter(QuestionMappingModel.mapping_id == mapping_id).first()
#     if db_mapping is None:
#         raise HTTPException(status_code=404, detail="QuestionMapping not found")
#     db.delete(db_mapping)
#     db.commit()
#     return {"message": "QuestionMapping deleted successfully"}

# # ------------------------------------------------------------------------------------------------------------------
#                         #paper  Table
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for Paper
# class PaperCreate(BaseModel):
#     title: str
#     description: str
#     user_id: int

# # Pydantic schema for Paper response
# class PaperResponse(BaseModel):
#     paper_id: int
#     title: str
#     description: str
#     user_id: int

# # Create Paper
# @router.post("/papers/", response_model=PaperResponse)
# def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
#     try:
#         db_paper = PaperModel(**paper.dict())
#         db.add(db_paper)
#         db.commit()
#         db.refresh(db_paper)
#         return db_paper
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# # Get Paper by ID
# @router.get("/papers/{paper_id}", response_model=PaperResponse)
# def get_paper(paper_id: int, db: Session = Depends(get_db)):
#     db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
#     if db_paper is None:
#         raise HTTPException(status_code=404, detail="Paper not found")
#     return db_paper

# # Update Paper
# @router.put("/papers/{paper_id}", response_model=PaperResponse)
# def update_paper(paper_id: int, paper: PaperCreate, db: Session = Depends(get_db)):
#     db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
#     if db_paper is None:
#         raise HTTPException(status_code=404, detail="Paper not found")
#     for key, value in paper.dict().items():
#         setattr(db_paper, key, value)
#     db.commit()
#     db.refresh(db_paper)
#     return db_paper

# # Delete Paper
# @router.delete("/papers/{paper_id}")
# def delete_paper(paper_id: int, db: Session = Depends(get_db)):
#     db_paper = db.query(PaperModel).filter(PaperModel.paper_id == paper_id).first()
#     if db_paper is None:
#         raise HTTPException(status_code=404, detail="Paper not found")
#     db.delete(db_paper)
#     db.commit()
#     return {"message": "Paper deleted successfully"}


# # ------------------------------------------------------------------------------------------------------------------
#                         #Teacher
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for Teacher
# class TeacherCreate(BaseModel):
#     name: str
#     email: str
#     department: str

# # Pydantic schema for Teacher response
# class TeacherResponse(BaseModel):
#     Teacher_id: int
#     name: str
#     email: str
#     department: str

# # Create Teacher
# @router.post("/teachers/", response_model=TeacherResponse)
# def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
#     db_teacher = TeacherModel(**teacher.dict())
#     db.add(db_teacher)
#     db.commit()
#     db.refresh(db_teacher)
#     return db_teacher

# # Get Teacher by ID
# @router.get("/teachers/{teacher_id}", response_model=TeacherResponse)
# def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return db_teacher

# # Update Teacher
# @router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
# def update_teacher(teacher_id: int, teacher: TeacherCreate, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     for key, value in teacher.dict().items():
#         setattr(db_teacher, key, value)
#     db.commit()
#     db.refresh(db_teacher)
#     return db_teacher

# # Delete Teacher
# @router.delete("/teachers/{teacher_id}")
# def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
#     db_teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_id == teacher_id).first()
#     if db_teacher is None:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     db.delete(db_teacher)
#     db.commit()
#     return {"message": "Teacher deleted successfully"}

# # ------------------------------------------------------------------------------------------------------------------
#                         #Course
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for Course
# class CourseCreate(BaseModel):
#     name: str
#     description: str

# # Pydantic schema for Course response
# class CourseResponse(BaseModel):
#     id: int
#     name: str
#     description: str

# # Create Course
# @router.post("/courses/", response_model=CourseResponse)
# def create_course(course: CourseCreate, db: Session = Depends(get_db)):
#     db_course = CourseModel(**course.dict())
#     db.add(db_course)
#     db.commit()
#     db.refresh(db_course)
#     return db_course

# # Get Course by ID
# @router.get("/courses/{course_id}", response_model=CourseResponse)
# def get_course(course_id: int, db: Session = Depends(get_db)):
#     db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
#     if db_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")
#     return db_course

# # Update Course
# @router.put("/courses/{course_id}", response_model=CourseResponse)
# def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
#     db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
#     if db_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")
#     for key, value in course.dict().items():
#         setattr(db_course, key, value)
#     db.commit()
#     db.refresh(db_course)
#     return db_course

# # Delete Course
# @router.delete("/courses/{course_id}")
# def delete_course(course_id: int, db: Session = Depends(get_db)):
#     db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
#     if db_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")
#     db.delete(db_course)
#     db.commit()
#     return {"message": "Course deleted successfully"}

# # ------------------------------------------------------------------------------------------------------------------
#                         #lession
# # ------------------------------------------------------------------------------------------------------------------
# # Pydantic schema for Lesson
# class LessonCreate(BaseModel):
#     title: str
#     description: str

# # Pydantic schema for Lesson response
# class LessonResponse(BaseModel):
#     lesson_id: int
#     title: str
#     description: str

# # Create Lesson
# @router.post("/lessons/", response_model=LessonResponse)
# def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
#     db_lesson = LessonModel(**lesson.dict())
#     db.add(db_lesson)
#     db.commit()
#     db.refresh(db_lesson)
#     return db_lesson
# # Get Lesson by ID
# @router.get("/lessons/{lesson_id}", response_model=LessonResponse)
# def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     return db_lesson

# # Update Lesson
# @router.put("/lessons/{lesson_id}", response_model=LessonResponse)
# def update_lesson(lesson_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     for key, value in lesson.dict().items():
#         setattr(db_lesson, key, value)
#     db.commit()
#     db.refresh(db_lesson)
#     return db_lesson

# # Delete Lesson
# @router.delete("/lessons/{lesson_id}")
# def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
#     db_lesson = db.query(LessonModel).filter(LessonModel.lesson_id == lesson_id).first()
#     if db_lesson is None:
#         raise HTTPException(status_code=404, detail="Lesson not found")
#     db.delete(db_lesson)
#     db.commit()
#     return {"message": "Lesson deleted successfully"}

# # ------------------------------------------------------------------------------------------------------------------
#                         #Module
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for Module
# class ModuleCreate(BaseModel):
#     name: str

# # Pydantic schema for Module response
# class ModuleResponse(BaseModel):
#     module_id: int
#     name: str

# # Create Module
# @router.post("/modules/", response_model=ModuleResponse)
# def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
#     db_module = ModuleModel(**module.dict())
#     db.add(db_module)
#     db.commit()
#     db.refresh(db_module)
#     return db_module

# # Get Module by ID
# @router.get("/modules/{module_id}", response_model=ModuleResponse)
# def get_module(module_id: int, db: Session = Depends(get_db)):
#     db_module = db.query(ModuleModel).filter(ModuleModel.module_id == module_id).first()
#     if db_module is None:
#         raise HTTPException(status_code=404, detail="Module not found")
#     return db_module

# # Update Module
# @router.put("/modules/{module_id}", response_model=ModuleResponse)
# def update_module(module_id: int, module: ModuleCreate, db: Session = Depends(get_db)):
#     db_module = db.query(ModuleModel).filter(ModuleModel.module_id == module_id).first()
#     if db_module is None:
#         raise HTTPException(status_code=404, detail="Module not found")
#     for key, value in module.dict().items():
#         setattr(db_module, key, value)
#     db.commit()
#     db.refresh(db_module)
#     return db_module

# # Delete Module
# @router.delete("/modules/{module_id}")
# def delete_module(module_id: int, db: Session = Depends(get_db)):
#     db_module = db.query(ModuleModel).filter(ModuleModel.module_id == module_id).first()
#     if db_module is None:
#         raise HTTPException(status_code=404, detail="Module not found")
#     db.delete(db_module)
#     db.commit()
#     return {"message": "Module deleted successfully"}


# # ------------------------------------------------------------------------------------------------------------------
#                         #Question
# # ------------------------------------------------------------------------------------------------------------------
# # Pydantic schema for Question
# class QuestionCreate(BaseModel):
#     question_text: str
#     question_image: Optional[str] = None
#     options1_text: str
#     options1_images: Optional[str] = None
#     options2_text: str
#     options2_images: Optional[str] = None
#     options3_text: str
#     options3_images: Optional[str] = None
#     options4_text: str
#     options4_images: Optional[str] = None
#     correct_answer_text: str
#     correct_answer_image: Optional[str] = None
#     difficulty_level: str


# class QuestionGetResponse(BaseModel):
#     question_id: int
#     question_text: str
#     question_image: Optional[str] = None
#     options1_text: str
#     options1_images: Optional[str] = None
#     options2_text: str
#     options2_images: Optional[str] = None
#     options3_text: str
#     options3_images: Optional[str] = None
#     options4_text: str
#     options4_images: Optional[str] = None
#     correct_answer_text: str
#     correct_answer_image: Optional[str] = None
#     difficulty_level: str

# # Function to save file

# def save_upload(upload_file: UploadFile) -> str:
#     unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
#     file_path = os.path.join("uploads", unique_filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(upload_file.file, buffer)
#     return file_path

# @router.post("/questions/", response_model=None)
# async def create_question(
#     question_text: str = Form(None),
#     question_image: UploadFile = File(default=None),
#     option1_text: str = Form(None),
#     option1_image: UploadFile = File(default=None),
#     option2_text: str = Form(None),
#     option2_image: UploadFile = File(default=None),
#     option3_text: str = Form(None),
#     option3_image: UploadFile = File(default=None),
#     option4_text: str = Form(None),
#     option4_image: UploadFile = File(default=None),
#     correct_answer_text: str = Form(None),
#     correct_answer_image: UploadFile = File(default=None),
#     difficulty_level: str = Form(None),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Save question and option images if provided
#         question_image_path = save_upload(question_image) if question_image else None
#         option1_image_path = save_upload(option1_image) if option1_image else None
#         option2_image_path = save_upload(option2_image) if option2_image else None
#         option3_image_path = save_upload(option3_image) if option3_image else None
#         option4_image_path = save_upload(option4_image) if option4_image else None
#         correct_answer_image_path = save_upload(correct_answer_image) if correct_answer_image else None

#         # Create Question instance
#         db_question = Question(
#             question_text=question_text,
#             question_images=question_image_path,
#             option1_text=option1_text,
#             option1_images=option1_image_path,
#             option2_text=option2_text,
#             option2_images=option2_image_path,
#             option3_text=option3_text,
#             option3_images=option3_image_path,
#             option4_text=option4_text,
#             option4_images=option4_image_path,
#             correct_ans_text=correct_answer_text,
#             correct_ans_images=correct_answer_image_path,
#             difficulty_level=difficulty_level
#         )

#         # Add to session and commit
#         db.add(db_question)
#         db.commit()
#         db.refresh(db_question)

#         return { "message ": 'question has been created succesfully'}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Get Question by ID
# @router.get("/questions/{question_id}", response_model=QuestionGetResponse)
# async def get_question(question_id: int, db: Session = Depends(get_db)):
#     try:
#         # Retrieve question from the database using the provided question_id
#         db_question = db.query(Question).filter(Question.question_id == question_id).first()
        
#         # Check if the question exists
#         if db_question is None:
#             raise HTTPException(status_code=404, detail="Question not found")
        
#         # Return the QuestionResponse
#         return {
#             "question_id": db_question.question_id,
#             "question_text": db_question.question_text,
#             "question_image": db_question.question_images,
#             "options1_text": db_question.option1_text,
#             "options1_images": db_question.option1_images,
#             "options2_text": db_question.option2_text,
#             "options2_images": db_question.option2_images,
#             "options3_text": db_question.option3_text,
#             "options3_images": db_question.option3_images,
#             "options4_text": db_question.option4_text,
#             "options4_images": db_question.option4_images,
#             "correct_answer_text": db_question.correct_ans_text,
#             "correct_answer_image": db_question.correct_ans_images,
#             "difficulty_level": db_question.difficulty_level
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # Update Question
# @router.put("/questions/{question_id}", response_model=None)
# async def update_question(
#     question_id: int,
#     question_text: str = Form(None),
#     question_image: UploadFile = File(default=None),
#     option1_text: str = Form(None),
#     option1_image: UploadFile = File(default=None),
#     option2_text: str = Form(None),
#     option2_image: UploadFile = File(default=None),
#     option3_text: str = Form(None),
#     option3_image: UploadFile = File(default=None),
#     option4_text: str = Form(None),
#     option4_image: UploadFile = File(default=None),
#     correct_answer_text: str = Form(None),
#     correct_answer_image: UploadFile = File(default=None),
#     difficulty_level: str = Form(None),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Retrieve the question from the database
#         db_question = db.query(Question).filter(Question.question_id == question_id).first()

#         # Check if the question exists
#         if db_question is None:
#             raise HTTPException(status_code=404, detail="Question not found")

#         # Update the question text and difficulty level if provided
#         if question_text:
#             db_question.question_text = question_text
#         if difficulty_level:
#             db_question.difficulty_level = difficulty_level

#         # Update image data if provided
#         if question_image:
#             question_image_path = save_upload(question_image)
#             db_question.question_images = question_image_path
#         if option1_image:
#             option1_image_path = save_upload(option1_image)
#             db_question.option1_images = option1_image_path
#         if option2_image:
#             option2_image_path = save_upload(option2_image)
#             db_question.option2_images = option2_image_path
#         if option3_image:
#             option3_image_path = save_upload(option3_image)
#             db_question.option3_images = option3_image_path
#         if option4_image:
#             option4_image_path = save_upload(option4_image)
#             db_question.option4_images = option4_image_path
#         if correct_answer_image:
#             correct_answer_image_path = save_upload(correct_answer_image)
#             db_question.correct_ans_images = correct_answer_image_path

#         # Commit the changes
#         db.commit()

#         return {"message": "Question has been updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # Delete Question
# @router.delete("/questions/{question_id}", response_model=None)
# async def delete_question(
#     question_id: int,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Retrieve the question from the database
#         db_question = db.query(Question).filter(Question.question_id == question_id).first()

#         # Check if the question exists
#         if db_question is None:
#             raise HTTPException(status_code=404, detail="Question not found")

#         # Delete the question from the database
#         db.delete(db_question)
#         db.commit()

#         return {"message": "Question has been deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# # ------------------------------------------------------------------------------------------------------------------
#                         #Test
# # ------------------------------------------------------------------------------------------------------------------

# # Pydantic schema for Test
# class TestCreate(BaseModel):
#     Description: str
#     teacher_id: int
#     students_id: int

# # Pydantic schema for Test response
# class TestResponse(BaseModel):
#     test_id: int
#     Description: str
#     teacher_id: int
#     students_id: int

# # Create Test
# @router.post("/tests/", response_model=TestResponse)
# def create_test(test: TestCreate, db: Session = Depends(get_db)):
#     db_test = TestModel(**test.dict())
#     db.add(db_test)
#     db.commit()
#     db.refresh(db_test)
#     return db_test

# # Get Test by ID
# @router.get("/tests/{test_id}", response_model=TestResponse)
# def get_test(test_id: int, db: Session = Depends(get_db)):
#     db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#     if db_test is None:
#         raise HTTPException(status_code=404, detail="Test not found")
#     return db_test

# # Update Test
# @router.put("/tests/{test_id}", response_model=TestResponse)
# def update_test(test_id: int, test: TestCreate, db: Session = Depends(get_db)):
#     db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#     if db_test is None:
#         raise HTTPException(status_code=404, detail="Test not found")
#     for key, value in test.dict().items():
#         setattr(db_test, key, value)
#     db.commit()
#     db.refresh(db_test)
#     return db_test

# # Delete Test
# @router.delete("/tests/{test_id}")
# def delete_test(test_id: int, db: Session = Depends(get_db)):
#     db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
#     if db_test is None:
#         raise HTTPException(status_code=404, detail="Test not found")
#     db.delete(db_test)
#     db.commit()
#     return {"message": "Test deleted successfully"}







