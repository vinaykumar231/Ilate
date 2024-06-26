from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import (companies_router, branches_router, usertypes_router, modules_router, designations_router,
                           users_router,  demo_router, demovideos_router, subjects_router,lessons_router,
                           standards_router, courses_router, admission_router, inquiry_router,payments_router,content_router,
                           batches_router, fees_router, tests_router,  questions_router, 
                           question_papers_router, parents_router, teachers_Data_router,installments_router,mail_router,announcement_router, teacher_course_router,course_active
)


#Teacher data Api Router
#from Teacher_data.Employee.api import (contact_info_router, education_router, skills_router, languages_spoken_router, emergency_contacts_router,
                                       #dependents_router, employees_router, managers_router)

####################################################################################
                        #for google login
###################################################################################
from fastapi import FastAPI, Request, Depends, HTTPException, APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse,JSONResponse
from sqlalchemy.orm import Session
import secrets
import logging
from api.models.user import LmsUsers
from db.session import get_db
##################################################################################
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
app.include_router(announcement_router, prefix="/api", tags=["Admin Routes"])
app.include_router(teacher_course_router, prefix="/api", tags=["Admin Routes"])

app.include_router(demo_router, prefix="/api", tags=["Student Routes"])
app.include_router(demovideos_router, prefix="/api", tags=["Student Routes"])
app.include_router(inquiry_router, prefix="/api", tags=["Student Routes"])
app.include_router(fees_router, prefix="/api", tags=["Student Routes"])
app.include_router(payments_router, prefix="/api", tags=["Student Routes"])
app.include_router(installments_router, prefix="/api", tags=["Student Routes"])
app.include_router(mail_router, prefix="/api", tags=["Student Routes"])
app.include_router(course_active, prefix="/api", tags=["Student Routes"])

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
app.include_router( parents_router, prefix="/api", tags=["parent_&_Admin Routes"])
app.include_router(teachers_Data_router, prefix="/api", tags=["Teacher_&_Admin Routes"])
app.include_router(admission_router, prefix="/api", tags=["Student_&_Admin Routes"])


##################################################################################################################
                        #for google login
##################################################################################################################

SECRET_KEY = "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"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Initialize OAuth configuration
oauth = OAuth()
oauth.register(
    name='google',
    client_id="1060983306336-bg15c4kcvbd51jjj0p08pd68rp7uis6l.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)

# Google login endpoint
@app.get("/login11")
async def google_login(request: Request):
    redirect_uri = request.url_for('auth')
    logging.info(f"Redirect URI for Google login: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Google callback endpoint
logging.basicConfig(level=logging.INFO)

@app.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        # Retrieve the token and user information
        token = await oauth.google.authorize_access_token(request)
        logging.info(f"Token retrieved: {token}")
        print("Token:", token)
        
        # Check if the id_token is present
        if 'id_token' not in token:
            print("ID token not found in the token response:", token)
            logging.error("ID token not found in the token response")
            raise HTTPException(status_code=400, detail="ID token not found in the token response")
        
        # Parse the ID token to get user information
        user_info = await oauth.google.parse_id_token(request, token)
        logging.info(f"User information: {user_info}")
        print("User Information:", user_info)

        # Handle authenticated user data here
        db_user = db.query(LmsUsers).filter(LmsUsers.user_email == user_info['email']).first()
        if not db_user:
            db_user = LmsUsers(
                email=user_info['email'],
                name=user_info['name'],
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)  # Refresh instance to get the updated fields
            logging.info(f"New user created: {db_user}")

        # After handling user data, redirect to a success page or home page
        return RedirectResponse(url="/")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=400, detail="Google authentication failed")

########################################################################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8001, reload=True, host='0.0.0.0')