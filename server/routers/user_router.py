from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models import session , User
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import user_schemas
from server.utils import hash_helper
router = APIRouter(prefix="/user", tags=["User CURD"])


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

