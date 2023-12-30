from fastapi import APIRouter, status, HTTPException, Depends
from server.models.models1 import session as db
from server.models.models import User
from server.utils import hash_helper, oauth2
from server.schemas import token_schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
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

    except SQLAlchemyError as e:
    # Handle the exception
        print(e)
        db.rollback()

    data = {"access_token": access_token, 
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

    