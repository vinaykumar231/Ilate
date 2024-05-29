from datetime import datetime, timedelta
import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_bearer import JWTBearer, get_user_id_from_token, is_admin, get_admin, get_current_user
from db.session import get_db, api_response
from ..models.user import LmsUsers
from ..schemas import LoginInput, ChangePassword, UserCreate, UpdateUser, UserType

router = APIRouter()

user_ops = LmsUsers()


def generate_token(data):
    exp = datetime.utcnow() + timedelta(days=1)
    token_payload = {'user_id': data['emp_id'], 'exp': exp}
    token = jwt.encode(token_payload, 'cat_walking_on_the street', algorithm='HS256')
    return token, exp


@router.post('/lms_login')
async def lms_login(credential: LoginInput):
    try:
        response = user_ops.lms_login(credential)
        return response
    except HTTPException as e:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@router.post("/insert/lms_user")
async def lms_register(data: UserCreate, db: Session = Depends(get_db)):
    return user_ops.lms_register(data.model_dump(), db)


# @router.put("/update/lms_user/{user_id}", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
# async def lms_user_update(user_data: UpdateUser, user_id: int, current_user: User = Depends(get_current_user),
#                           db: Session = Depends(get_db)):
#     return user_ops.lms_user_update(user_data, user_id, db)

# @router.put("/update/lms_user/{user_id}", dependencies=[Depends(JWTBearer())])
# async def lms_user_update(user_data: UpdateUser, user_id: int,
#                           current_user: LmsUsers = Depends(get_current_user),
#                           db: Session = Depends(get_db)):
#     try:
#         if user_data.user_type and user_data.user_type not in {"user", "teacher", "admin"}:
#             raise HTTPException(status_code=403, detail="Invalid user type. Allowed values: user, teacher, admin")
#
#         if current_user.user_type == "admin" or current_user.user_id == user_id:
#             if user_data.current_password:
#                 if not user_ops.validate_password(user_data.current_password):
#                     raise HTTPException(status_code=400, detail="Invalid current password")
#
#                 if user_data.new_password:
#                     user_ops.change_password(user_data.current_password, user_data.new_password, user_id, db)
#         else:
#             raise HTTPException(status_code=403, detail="Forbidden: You are not authorized to update this user's data.")
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=f"Error: {str(e)}")

#Nikunj

@router.get("/read/lms_user", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
async def searchall(user_id: int = None, user_type: UserType = None, page_num: int = 1, page_size: int = 20,
                    db: Session = Depends(get_db)):
    return user_ops.searchall(user_id, user_type, page_num, page_size, db)


@router.get("/get_my_profile")
def get_current_user_details(current_user: LmsUsers = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_details = {
            "user_id": current_user.user_id,
            "username": current_user.user_name,
            "email": current_user.user_email,
            "user_type": current_user.user_type,
            "is_formsubmited": current_user.is_formsubmited,
            "is_payment_done": current_user.is_payment_done,
            "created_on": current_user.created_on,

        }
        return api_response(data=user_details, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/update/lms_user/{user_id}", dependencies=[Depends(JWTBearer())])
async def lms_user_update(user_data: UpdateUser, user_id: int,
                          current_user: LmsUsers = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    try:
        if user_data.user_type and user_data.user_type not in {"user", "admin", "teacher", "student", "parent"}:
            raise HTTPException(status_code=403, detail="Invalid user type. Allowed values: user, admin, teacher, student, parent")

        if current_user.user_type == "admin" or current_user.user_id == user_id:
            db_user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id, LmsUsers.is_deleted == False).first()
            if db_user is None:
                raise HTTPException(status_code=404, detail="Record not found")

            if user_data.user_email:
                existing_user = db.query(LmsUsers).filter(
                    LmsUsers.user_email == user_data.user_email,
                    LmsUsers.user_id != user_id
                ).first()
                if existing_user:
                    raise HTTPException(status_code=400, detail="Email already exists for another user")

            hero_data = user_data.dict(exclude_unset=True)
            for key, value in hero_data.items():
                setattr(db_user, key, value)

            is_administrator: bool = current_user.user_type == "admin"

            if (is_administrator and user_data.new_password) or (
                    not is_administrator and user_data.current_password and user_data.new_password):
                if not user_ops.validate_password(user_data.new_password):
                    raise HTTPException(status_code=400, detail="Invalid new password")

                current_password = None if is_administrator else user_data.current_password
                user_ops.change_password(current_password, user_data.new_password, user_id, is_administrator, db)

            db.commit()
            response = api_response(200, message="User Data updated successfully")
            return response
        else:
            raise HTTPException(status_code=403, detail="Forbidden: You are not authorized to update this user's data.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")




# @router.get("/get_my_profile", dependencies=[Depends(JWTBearer())])
# async def get_current_user_details(current_user: LmsUsers = Depends(get_current_user), db: Session = Depends(get_db)):
#     user_id = current_user.user_id
#     return user_ops.lms_user_update(user_id, db)


# @router.post('/update/change_password', dependencies=[Depends(JWTBearer())])
# async def change_password(credential: ChangePassword, user_id: int = Depends(get_user_id_from_token),
#                           db: Session = Depends(get_db)):
#     return user_ops.change_password(credential, user_id, db)

# @router.put("/admin/usertype_change", dependencies=[Depends(JWTBearer()), Depends(get_admin)])
# def change_user_type(user_id: int, new_user_type: UserType, db: Session = Depends(get_db)):
#     user = db.query(LmsUsers).filter(LmsUsers.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.user_type = new_user_type.value
#     db.commit()
#
#     return {"message": f"User type changed to {new_user_type}"}
