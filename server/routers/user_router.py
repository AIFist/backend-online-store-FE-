from fastapi import Body, status,HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import User
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import user_schemas
from server.utils import hash_helper
router = APIRouter(prefix="/user", tags=["User CRUD"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user_data:user_schemas.GetUser = Body(...)):
    """
    This endpoint to create user in the database 

    Args:
        user_data (user_schemas.GetUser, optional): Username, email 
        and passsward will be getting by this varible
        

    Returns:
        User: It will return user's data that has beeing created
    """
    
    # hashing the passward 
    hashed_password = hash_helper.hash(user_data.password)
    user_data.password = hashed_password
    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post('/login')
def login(user_credentials:user_schemas.AuthUser):
    user = session.query(User).filter(
        User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    if not hash_helper.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    # access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return {"access_token": access_token, "token_type": "bearer"}
    return {"message": "Welcame and Happy Shopping"}
