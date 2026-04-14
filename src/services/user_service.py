from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from src.services import user_service
from src.database import psycopg

# Load environment variables from .env file
load_dotenv()
cursor = psycopg.cursor
conn = psycopg.conn


# Access the variables using os.getenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 
#this tokenUrl="login" means that whenever we use the "Depends(oauth2_scheme)" it will go to the login endpoint and take the token from there
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = user_service.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)): #it is going to verify that the verify_acess_token's user
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate credentials, bro", headers={"WWW-Authenticate": "Bearer"})  
    try:
        token_data = verify_access_token(token, credentials_exception)
        cursor.execute("""SELECT * from users WHERE user_id = %s """, (token_data.id,))
        user = cursor.fetchone()
        if user is None:
            raise credentials_exception
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")
