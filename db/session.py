from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/LMS_21_June"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres.fjubgwysqgxcedhwhvdu:y5pD2C5abBLMQjVN@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def api_response(status_code, data=None, message: str = None, total: int = 0, count: int = 0):
    response_data = {"data": data, "message": message, "status_code": status_code, "total": total, "count": count}
    filtered_response = {key: value for key, value in response_data.items() if value is not None or 0}
    return filtered_response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()