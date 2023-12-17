from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from dotenv import load_dotenv
from server.schemas import token_schemas
from server.models.models1 import session as db
from server.models.models import User
import os
load_dotenv()


DB_URL: str = os.getenv("DB")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# secret key
# Algorithm
# expiertion time
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exeception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exeception

        token_data = token_schemas.TokenData(id=id)
    except (jwt.JWTError, ValidationError):
        raise credentials_exeception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not varify the credentails", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # print(token.id)
    user = db.query(User).filter(User.id == token.id).first()

    return user