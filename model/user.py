from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str    
    salary: str | None = None
    promotion_date: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
