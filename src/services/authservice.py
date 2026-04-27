from src.schemas import users_models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.services import user_service
from src.models.models import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def create_user(user: users_models.UserCreate, db: Session) -> User:
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def verify_user(user_credentials: users_models.UserLogin, db: Session):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if user is None or not verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = user_service.create_access_token(data={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
