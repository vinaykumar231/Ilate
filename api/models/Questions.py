# from sqlalchemy import Column, Integer, String, ForeignKey
# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import relationship
# from db.base import Base
# from typing import List, Optional
# from fastapi import Form
# import shutil
# import uuid
# import os
# from .Test import Test


# class Question(Base):
#     __tablename__ = 'questions'

#     question_id = Column(Integer, primary_key=True)
#     question_text = Column(String(255))
#     question_images = Column(String(255))
#     option1_text = Column(String(255))
#     option1_images = Column(String(255))
#     option2_text = Column(String(255))
#     option2_images = Column(String(255))
#     option3_text = Column(String(255))
#     option3_images = Column(String(255))
#     option4_text = Column(String(255))
#     option4_images = Column(String(255))
#     given_ans_text = Column(String(255))
#     given_ans_image = Column(String(255))
#     correct_ans_text = Column(String(255))
#     correct_ans_images = Column(String(255))
#     difficulty_level = Column(String(255))
#     test_id = Column(Integer, ForeignKey('tests.test_id'))

#     mappings = relationship("QuestionMapping", back_populates="question")

#     tests = relationship("Test", back_populates="question")



# # Function to save file

# def save_upload(upload_file: UploadFile) -> str:
#     unique_filename = str(uuid.uuid4()) + "_" + upload_file.filename
#     file_path = os.path.join("uploads", unique_filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(upload_file.file, buffer)
#     return file_path