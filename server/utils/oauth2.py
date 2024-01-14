from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from dotenv import load_dotenv
from server.schemas import token_schemas
from server.models.models1 import session as db
from server.models.models import User


# following code is for debugging
# import logging
# logging.basicConfig(level=logging.DEBUG)
import os
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# secret key
# Algorithm
# expiertion time
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_DAY = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAY"))

def create_access_token(data: dict):
    """
    Generate an access token using the provided data.
    Args:
        data (Dict[str, str]): The data to be encoded in the access token.
    Returns:
        str: The generated access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Create a refresh token.

    Args:
        data (dict): A dictionary containing the data to be encoded in the token.

    Returns:
        str: The encoded refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exeception):
    """
    Verifies the access token provided.

    Parameters:
        token (str): The access token to be verified.
        credentials_exception (Exception): The exception to be raised if the credentials are invalid.

    Returns:
        TokenData: The token data containing the user's ID.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        role : str = payload.get("role")
       
        id = str(id)
        if id is None:
            print(" Id error ")
            raise credentials_exeception


        token_data = token_schemas.TokenData(id=id)
    except (jwt.JWTError, ValidationError) as e:
         # following comment is for debugging
        # print("JWT error ")
        # logging.exception("Error during JWT processing or validation: %s", str(e))
        print(e)
        raise credentials_exeception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided token.

    Parameters:
    - token (str): The access token used to authenticate the user. Defaults to `Depends(oauth2_scheme)`.

    Returns:
    - user: The user object associated with the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not varify the credentails", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # print(token.id)
    user = db.query(User).filter(User.id == token.id).first()

    return user

# Function to decode JWT token
def decode_jwt_token(token: str):
    """
    Decode a JWT token and retrieve the email from its payload.

    Parameters:
        token (str): The JWT token to decode.

    Returns:
        str: The email retrieved from the JWT token payload.

    Raises:
        HTTPException: If the token cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception