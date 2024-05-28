from jose import jwt, exceptions
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone


class CredentialsException(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}):
        self.status_code=status_code
        self.detail=detail
        self.headers=headers


SECRET_KEY = "7243a26db371de387beee5e6ef6ddc78cb51d92b07ff27c873fe68bc30e6005e"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: None = None) -> str:
    
    """Принимает словарь с юзернеймом возвращает jwt-токен
    data = {'sub': 'username'}"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

token = create_access_token({'sub': 'username'})
token = create_access_token({'sub1': 'username'}) #JWEInvalidAuth
#token = '' #JWTError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
            raise CredentialsException
    print(payload)
except exceptions.JWTError:
    print('==============raising from except============')
    raise CredentialsException

print('===========here================')