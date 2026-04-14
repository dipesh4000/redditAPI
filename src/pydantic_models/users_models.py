from pydantic import BaseModel, EmailStr
from datetime import datetime, time
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str