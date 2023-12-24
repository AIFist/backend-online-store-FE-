# Import necessary libraries
from fastapi import  HTTPException, status, APIRouter
from server.utils import oauth2
# Assuming you have a user model
from server.models.models1 import session
from server.db import reset_password_helper


router = APIRouter(prefix="/reset", tags=["For reseting password"])



# Route to initiate password reset
@router.post("/password-reset/{email}", response_model=dict)
async def initiate_password_reset(email: str):
    # Check if email exists in the database
    user = reset_password_helper.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    # Generate a unique token and send it to the user's email
    token_data = {"sub": email}
    token = oauth2.create_access_token(token_data)
    reset_password_helper.send_reset_email(email, token)

    return {"message": "Password reset initiated"}
    # return {"message": token}

