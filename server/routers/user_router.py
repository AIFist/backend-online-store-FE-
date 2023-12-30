from fastapi import Body, status,HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import User
from server.schemas import user_schemas
from server.utils import hash_helper
from server.utils import oauth2
router = APIRouter(prefix="/user", tags=[" ------------------------ Required User Role ------------------------ \nUser CRUD"])


@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_model=user_schemas.GetUserResponse
             )
async def create_user(user_data: user_schemas.GetUser = Body(...)):
    """
    Create a new user in the database.

    Args:
        user_data (user_schemas.GetUser): The user data including username, email, and password.

    Returns:
        User: The created user data.
    """

    email_exists = session.query(User).filter(User.email == user_data.email).first()
    username_exists = session.query(User).filter(User.username == user_data.username).first() 
    if email_exists and username_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email and Username already registered")
    if username_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
        
    
    if email_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    try:
       
        # Hash the password
        hashed_password = hash_helper.hash(user_data.password)
        user_data.password = hashed_password

        # Create a new User object
        user = User(**user_data.model_dump())

        # Add the user to the session and commit the changes
        session.add(user)
        session.commit()
        session.refresh(user)
        access_token = oauth2.create_access_token(data={"user_id": user.id, "role": user.role})
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "billing_address": user.billing_address,
            "shipping_address": user.shipping_address,
            "access_token": access_token
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return user_data


@router.put("/update/{id}", status_code=status.HTTP_201_CREATED)
async def update_user(id: int, user_update: user_schemas.UpdateUser = Body(...)):
    """
    Note: this is not working
    Update the username and email of a user.

    Args:
    - id (int): The primary key of the user.
    - user_update (user_schemas.UpdateUser, optional): The updated username and email in JSON format.

    Raises:
        HTTPException: If a user with the given id does not exist, it returns a 404 status code.

    Returns:
        JSON: The updated user's data.
    """
    pass
    