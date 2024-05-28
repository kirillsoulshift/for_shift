from fastapi import HTTPException, status

class MissingUser(Exception):
    def __init__(self, msg:str):
        self.msg = msg


class UnathenticatedUser(Exception):
    def __init__(self, msg:str):
        self.msg = msg


class CredentialsException(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось проверить учетные данные",
                headers={"WWW-Authenticate": "Bearer"}):
        self.status_code=status_code
        self.detail=detail
        self.headers=headers

class WrongPasswordException(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"}):
        self.status_code=status_code
        self.detail=detail
        self.headers=headers