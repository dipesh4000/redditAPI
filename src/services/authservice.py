from src.pydantic_models import users_models as users_models
from passlib.context import CryptContext
from src.database import psycopg
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.services import user_service

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


cursor = psycopg.cursor
conn = psycopg.conn

def create_user(user: users_models.UserCreate):
    print(user)
    hashed_password = hash(user.password)
    try:
        cursor.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING * """,
                       (user.username, hashed_password, user.email))
        new_user = cursor.fetchone()
        conn.commit()
        return new_user
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    

def verify_user(user_credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        cursor.execute("""SELECT * from users WHERE username = %s """, (user_credentials.username,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if not verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        access_token = user_service.create_access_token(data={"user_id": user.user_id})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")

    