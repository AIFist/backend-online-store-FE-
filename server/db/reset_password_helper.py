from server.models.models import User
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

password: str = os.getenv("password")
email1: str = os.getenv("email")


def get_user_by_email(session, email: str):
    user_query = session.query(User).filter(User.email == email)
    user = user_query.first()
    if user:
        return True
    return False





def send_reset_email(email: str, token: str):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = email1
    smtp_password = password

    # Email content
    subject = "Password Reset"
    body = f"Click the following link to reset your password: http://your-app.com/reset-password?token={token}"

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

