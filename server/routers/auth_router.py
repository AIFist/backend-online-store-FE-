from fastapi import APIRouter, status, HTTPException, Depends
from server.models.models1 import session as db
from server.models.models import User
from server.utils import hash_helper, oauth2
from server.schemas import token_schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    # Query the database to find the user with the given email
    user = db.query(User).filter(User.email == user_credentials.username).first()

    # If user is not found, raise an HTTPException with a 403 status code and an error message
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # If the password is incorrect, raise an HTTPException with a 403 status code and an error message
    if not hash_helper.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Generate an access token using the oauth2 library, passing the user_id as data
    access_token = oauth2.create_access_token(data={"user_id": user.id, "role": user.role})

    # Return the access token and the token type as a dictionary
    return {"access_token": access_token, "token_type": "bearer"}
