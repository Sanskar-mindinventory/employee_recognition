from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.v1.user_authentication.schemas.user_schemas import UserRegistrationRequestSchema, UserLoginRequestSchema, \
    UserResponseSchema, UserUpdateSchema
from src.api.v1.user_authentication.services.user_services import UserServices
from database.database import get_db
from src.api.v1.user_authentication.utils.auth_utils import get_current_active_user, get_current_user

user_api_router = APIRouter(
    prefix="/user",
)


@user_api_router.get("/secure-data/", status_code=200)
def get_secure_data(current_user: UserResponseSchema = Depends(get_current_active_user)):
    return UserServices.test_api(current_user)


@user_api_router.post("/register", status_code=201)
def register_user(request: UserRegistrationRequestSchema, db: Session = Depends(get_db)):
    return UserServices.register(request=request, db_session=db)


@user_api_router.post("/token", status_code=200)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserServices.get_token(form_data=form_data, db_session=db)


@user_api_router.post("/login", status_code=200)
def login_user(request: UserLoginRequestSchema, db: Session = Depends(get_db)):
    return UserServices.login(request=request, db_session=db)


@user_api_router.post("/update/{user_id}", status_code=200)
def update_user(user_id: Annotated[int, Path(title='Please Enter User ID for the updation')],request:UserUpdateSchema, current_user:UserResponseSchema= Depends(get_current_active_user), db:Session=Depends(get_db)):
    return UserServices.update_user(request=request, user_id=user_id, db_session=db, current_user=current_user)