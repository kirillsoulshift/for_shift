from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, exceptions
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model.user import UserInDB, TokenData
from model.error import MissingUser, UnathenticatedUser, CredentialsException

SECRET_KEY = "7243a26db371de387beee5e6ef6ddc78cb51d92b07ff27c873fe68bc30e6005e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    'user1': {
        'username': 'user1',
        'salary': '60000',
        'promotion_date': '12.12.2024',        
        "disabled": False,
        'hashed_password': pwd_context.hash('secret1'),
    },
    'user2': {
        'username': 'user2',
        'salary': '80000',
        'promotion_date': '12.11.2024',        
        "disabled": True,
        'hashed_password': pwd_context.hash('secret2'),
    }
}

def get_user(name: str) -> UserInDB:
    user = fake_users_db.get(name)
    if not user:
        return None
    return UserInDB(**user)

def authenticate_user(username: str, password: str) -> UserInDB:

    """Принимает юзернейм и пароль сравнивает с сохраненным хешом и возвращает UserInDB"""
    
    user = get_user(username)
    if not user:
        raise MissingUser(msg=f'User {username} not found')
    if not pwd_context.verify(password, user.hashed_password):
        raise UnathenticatedUser(msg=f'Wrong username or password')
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    
    """Принимает словарь с юзернеймом возвращает jwt-токен"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    
    """ 1 Получает jwt токен 
        2 декодирует его
        3 извлекает юзернейм
        4 по юзернейму получает объект UserInDB
        5 вернуть объект UserInDB
        """
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except exceptions.JWTError:
        raise CredentialsException
    user = get_user(username=token_data.username)
    if user is None:
        raise MissingUser(msg=f'User {username} not found')
    return user