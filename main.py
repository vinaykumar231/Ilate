from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import (companies_router, branches_router, usertypes_router, modules_router, designations_router,
                           users_router, students_router, demo_router, demovideos_router, subjects_router,
                           standards_router, courses_router, admission_router, inquiry_router, payment_router)
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


app.include_router(companies_router, prefix="/api")
app.include_router(branches_router, prefix="/api")
app.include_router(users_router, prefix="/api")
# app.include_router(usertypes_router, prefix="/api")
app.include_router(students_router, prefix="/api")
#app.include_router(modules_router, prefix="/api")
#app.include_router(designations_router, prefix="/api")
app.include_router(courses_router, prefix="/api")
app.include_router(subjects_router, prefix="/api")
app.include_router(demo_router, prefix="/api")
app.include_router(demovideos_router, prefix="/api")
app.include_router(standards_router, prefix="/api")
app.include_router(admission_router, prefix="/api")
app.include_router(inquiry_router, prefix="/api")
app.include_router(payment_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)