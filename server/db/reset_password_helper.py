from server.models.models import User
import smtplib
from server.utils import hash_helper
from email.mime.text import MIMEText
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from fastapi import status, HTTPException
load_dotenv()

password: str = os.getenv("password")
email1: str = os.getenv("email")


def get_user_by_email(session, email: str):
    """
    Retrieves a user from the session by their email.

    Args:
        session: The database session.
        email: The email of the user to retrieve.

    Returns:
        The user with the specified email, or None if no user is found.
    """
    try:
        # Create a query to retrieve the user with the specified email
        user_query = session.query(User).filter(User.email == email)

        # Retrieve the first user from the query
        user = user_query.first()

        # Return the user
        return user
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably user with email {email} does not exist."
        )


# Function to update user password
def update_user_password(session, user: User, new_password: str):
    """
    Update the user's password in the database.

    Args:
        session: The database session.
        user: The user object.
        new_password: The new password to be set.

    Returns:
        None
    """
    try:
        # Hash the new password
        hashed_password = hash_helper.hash(new_password)

        # Update the user's hashed password
        user.password = hashed_password

        # Commit changes to the database
        session.add(user)
        session.commit()
        session.refresh(user)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably user with email {user.email} does not exist."
        )



def send_reset_email(email: str, token: str):
    """
    Send a password reset email to the specified email address.

    Args:
        email (str): The recipient's email address.
        token (str): The password reset token.

    Returns:
        None

    Raises:
        Exception: If there is an error sending the email.
    """

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = email1
    smtp_password = password

    # Email content
    subject = "Password Reset"
    
    body = f"Click the following link to reset your password: http://localhost:60602/reset-password?token={token}"


    # Create MIMEText object
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = smtp_username
    message["To"] = email

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, [email], message.as_string())

        # Disconnect from the SMTP server
        server.quit()

        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Error sending password reset email: {e}")

