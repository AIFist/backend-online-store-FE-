from fastapi import APIRouter, status, HTTPException, Depends
from server.models.models1 import session as db
from server.models.models import User
from server.utils import hash_helper, oauth2
from server.schemas import token_schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt,JWTError
from pydantic import ValidationError

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login.

    Args:
        user_credentials (OAuth2PasswordRequestForm): User credentials form.

    Returns:
        token_schemas.Token: Token response model.

    Raises:
        HTTPException: If user is not found or credentials are invalid.
        ValueError: If there is an error validating the token data.
    """
    try:
        # Query the database to find the user with the given email
        user = db.query(User).filter(User.email == user_credentials.username).first()

        # If user is not found, raise an HTTPException with a 403 status code and an error message
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

        if not hash_helper.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

        # Generate an access token using the oauth2 library, passing the user_id as data
        access_token = oauth2.create_access_token(data={"user_id": user.id, "role": user.role})
        # Generate an Refresh token using the oauth2 library, passing the user_id as data
        refresh_token = oauth2.create_refresh_token(data={"user_id": user.id, "role": user.role})

    except SQLAlchemyError as e:
        # Handle the exception
        print(e)
        db.rollback()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate access token")

    data = {"access_token": access_token,
            "refresh_token": refresh_token, 
            "token_type": "bearer",
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "role": user.role,
            "billing_address": user.billing_address, 
            "shipping_address": user.shipping_address
            }
    try:
        data_model = token_schemas.Token.model_validate(data)
        # Return the access token and the token type as a dictionary
        return data_model
    except ValueError as e:
        print(f"An error occurred: {e}")


@router.post("/refresh-token")
async def refresh_token(refresh_token: str = Depends(oauth2.oauth2_scheme)):
    """
    Refreshes the access token using a refresh token.

    Parameters:
        refresh_token (str): The refresh token used to generate a new access token.

    Returns:
        dict: A dictionary containing the new access token and the token type.
    """
    # Handle exceptions for invalid credentials
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")
        
        if user_id is None:
            raise credentials_exception

        if role is None:
            raise credentials_exception
        
        # Create token data object
        token_data = token_schemas.TokenData(id=str(user_id))
    
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # Create a new access token
    new_access_token = oauth2.create_access_token(data={"user_id": int(user_id), "role": role})
    
    # Return the new access token and token type
    return {"access_token": new_access_token, "token_type": "bearer"}
    
    