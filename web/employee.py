import os
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import Token, User
from model.error import MissingUser, UnathenticatedUser, WrongPasswordException
if os.getenv("UNIT_TEST"):
    from fake import employee as service
else:
    from service import employee as service

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """ 1 взять данные из формы - юзернейм и пароль
        2 верифицировать их 
        3 создать jwt
        4 вернуть jwt"""
    try:
        user = service.authenticate_user(form_data.username, form_data.password)
    except MissingUser:    
        raise WrongPasswordException
    except UnathenticatedUser:    
        raise WrongPasswordException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
def read_users_me(
    current_user: Annotated[User, Depends(service.get_current_user)]) -> User:
    """Возвращает данные активного юзера"""
    return current_user