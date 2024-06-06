from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import (companies_router, branches_router, usertypes_router, modules_router, designations_router,
                           users_router,  demo_router, demovideos_router, subjects_router,lessons_router,
                           standards_router, courses_router, admission_router, inquiry_router,payments_router,content_router,
                           batches_router, fees_router, tests_router,  questions_router, 
                           question_papers_router, parents_router, teachers_Data_router,installments_router,mail_router
)

#Teacher data Api Router
#from Teacher_data.Employee.api import (contact_info_router, education_router, skills_router, languages_spoken_router, emergency_contacts_router,
                                       #dependents_router, employees_router, managers_router)

from db.base import Base
from db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


app.include_router(companies_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(branches_router, prefix="/api")
# app.include_router(usertypes_router, prefix="/api")
# app.include_router(students_router, prefix="/api")
# app.include_router(designations_router, prefix="/api")
app.include_router(courses_router, prefix="/api", tags=["Admin Routes"])
app.include_router(standards_router, prefix="/api", tags=["Admin Routes"])
app.include_router(subjects_router, prefix="/api", tags=["Admin Routes"])
app.include_router(modules_router, prefix="/api", tags=["Admin Routes"])
app.include_router(lessons_router, prefix="/api", tags=["Admin Routes"])
app.include_router(content_router, prefix="/api", tags=["Admin Routes"])
app.include_router(tests_router, prefix="/api", tags=["Admin Routes"])
app.include_router(batches_router, prefix="/api", tags=["Admin Routes"])

app.include_router(questions_router, prefix="/api", tags=["Admin Routes"])
app.include_router(question_papers_router, prefix="/api", tags=["Admin Routes"])
app.include_router( parents_router, prefix="/api", tags=["Admin Routes"])


app.include_router(demo_router, prefix="/api", tags=["Student Routes"])
app.include_router(demovideos_router, prefix="/api", tags=["Student Routes"])
app.include_router(inquiry_router, prefix="/api", tags=["Student Routes"])
app.include_router(fees_router, prefix="/api", tags=["Student Routes"])
app.include_router(payments_router, prefix="/api", tags=["Student Routes"])
app.include_router(installments_router, prefix="/api", tags=["Student Routes"])
app.include_router(mail_router, prefix="/api", tags=["Student Routes"])

#app.include_router(inquiry_router, prefix="/api", tags=["Student Routes"])
#app.include_router(fees_router, prefix="/api")

#app.include_router(teachers_router, prefix="/api")
#app.include_router(students_router, prefix="/api", tags=["Student Routes"])
# app.include_router(payment_router, prefix="/api")

#Teacher all data
# app.include_router(contact_info_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(education_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(skills_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(languages_spoken_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(emergency_contacts_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router( dependents_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(employees_router, prefix="/api", tags=["Teacher_Employee Routes"])
# app.include_router(managers_router, prefix="/api", tags=["Teacher_Employee Routes"])
app.include_router(teachers_Data_router, prefix="/api", tags=["Teacher_&_Admin Routes"])
app.include_router(admission_router, prefix="/api", tags=["Student_&_Admin Routes"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8001, reload=True, host='0.0.0.0')