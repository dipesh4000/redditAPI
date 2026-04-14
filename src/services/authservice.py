from src.schemas import users_models
from passlib.context import CryptContext
from src.database import psycopg
from fastapi import HTTPException, status
from src.services import user_service

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(user: users_models.UserCreate):
    hashed_password = hash(user.password)
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING username, email, created_at",
                (user.username, hashed_password, user.email),
            )
            new_user = cursor.fetchone()
        conn.commit()
        return new_user
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)


def verify_user(user_credentials: users_models.UserLogin):
    conn = psycopg.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (user_credentials.username,))
            user = cursor.fetchone()
        if user is None or not verify(user_credentials.password, user["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = user_service.create_access_token(data={"user_id": user["user_id"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
    finally:
        psycopg.release_connection(conn)
