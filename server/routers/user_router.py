from fastapi import Body, status,HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import User
from server.schemas import user_schemas
from server.utils import hash_helper
router = APIRouter(prefix="/user", tags=[" ------------------------ Required User Role ------------------------ \nUser CRUD"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: user_schemas.GetUser = Body(...)):
    """
    Create a new user in the database.

    Args:
        user_data (user_schemas.GetUser): The user data including username, email, and password.

    Returns:
        User: The created user data.
    """
    user_exists = session.query(User).filter(User.username == user_data.username).first() or session.query(User).filter(User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already registered")

    # Hash the password
    hashed_password = hash_helper.hash(user_data.password)
    user_data.password = hashed_password

    # Create a new User object
    user = User(**user_data.model_dump())

    # Add the user to the session and commit the changes
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

# @router.post('/login')
# async def login(user_credentials: user_schemas.AuthUser):
#     """
#     Endpoint for user login. User provides email and password.

#     Args:
#         user_credentials (user_schemas.AuthUser): JSON object containing email and password.

#     Raises:
#         HTTPException: When invalid credentials are provided.

#     Returns:
#         dict: A dictionary with a "message" key indicating successful login.
#     """
#     # Query the user from the database based on the provided email
#     user = session.query(User).filter(User.email == user_credentials.email).first()

#     # Check if the user exists
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

#     # Verify the password using the hash_helper.verify() function
#     if not hash_helper.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

#     # Return a dictionary with a "message" key indicating successful login
#     return {"message": "Welcome and Happy Shopping"}


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
    # # Query the user by id
    # user_query = session.query(User).filter(User.id == id)
    # user = user_query.first()

    # # If user does not exist, raise an exception
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    # # Update the user data
    # user_query.update(user_update.model_dump(), synchronize_session=False)
    # session.commit()

    # # Return the updated user's data
    # return user_query.first()
