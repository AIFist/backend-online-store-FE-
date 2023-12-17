from fastapi import APIRouter, status, HTTPException, Depends
from server.models.models1 import session as db
from server.models.models import User
from server.utils import hash_helper, oauth2
from server.schemas import token_schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(
        User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    if not hash_helper.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    
    # Generate JWT token but Ishaque have to add user role in jwt token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}