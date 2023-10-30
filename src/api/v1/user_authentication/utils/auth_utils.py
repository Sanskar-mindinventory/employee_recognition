from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.api.v1.user_authentication.models.user_models import User
from src.api.v1.user_authentication.schemas.user_schemas import UserResponseSchema, RoleChoices
from database.database import get_db
from config.config import JWTSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user-authentication/user/token")

secret_key = JWTSettings().authjwt_secret_key
algorithm = JWTSettings().JWT_ALGORITHM


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = User.get_user_by_username(db_session=db, user_name=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserResponseSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def active_user_is_admin(current_user: UserResponseSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    if current_user.role not in {RoleChoices.Admin, RoleChoices.SuperAdmin}:
        raise HTTPException(status_code=400, detail=f"You are not authorised to perform this action. {current_user.email} has not permissions for this tasks.")
    return current_user                         
    