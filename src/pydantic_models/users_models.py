from pydantic import BaseModel, EmailStr
from datetime import datetime, time
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

