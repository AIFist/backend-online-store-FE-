# Import necessary libraries
from fastapi import  HTTPException, status, APIRouter, Body
from server.utils import oauth2
# Assuming you have a user model
from server.models.models1 import session
from server.db import reset_password_helper
from server.schemas import reset_password_schemas

router = APIRouter(prefix="/reset", tags=["For reseting password"])


# Route to initiate password reset
@router.post("/forget_password", response_model=dict)
async def initiate_password_reset(data: reset_password_schemas.ResetPasswordRequest = Body(...)):
    """
    Initiate a password reset for the given email.
    
    Args:
        data: The request body containing the email address.
        
    Raises:
        HTTPException: If the email is not found in the database.
    """
    # Check if email exists in the database
    user = reset_password_helper.get_user_by_email(session=session, email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    # Generate a unique token and send it to the user's email
    token_data = {"sub": data.email}
    token = oauth2.create_access_token(token_data)
    reset_password_helper.send_reset_email(data.email, token)
    
    return {"message": "Password reset initiated"}


@router.post("/reset-password",
             response_model=dict,
             status_code=status.HTTP_201_CREATED
             )
async def reset_password(data: reset_password_schemas.ResetPassword = Body(...)):
    """
    Reset the user's password using the provided token.

    Args:
        data (reset_password_schemas.ResetPassword): The data required to reset the password.

    Returns:
        dict: A dictionary with the message "Password reset successfully" if the password reset was successful.

    Raises:
        HTTPException: If the user is not found.
    """
    email = oauth2.decode_jwt_token(data.token)

    # Perform password reset in your database
    # For example, update the user's password
    user = reset_password_helper.get_user_by_email(session=session, email=email)
    if user:
        isVaildToken = reset_password_helper.check_token_validity(session=session,token=data.token)
        if isVaildToken:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is no longer valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
            
    if user:
        # Update the user's password
        reset_password_helper.update_user_password(session=session, user=user, new_password=data.new_password)
        reset_password_helper.add_token_blacklist(session=session,token=data.token, user_id=user.id)
        return {"message": "Password reset successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
