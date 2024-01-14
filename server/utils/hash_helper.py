from passlib.context import CryptContext
import logging
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str)-> str:
    """
    Generates a hash for the given password.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    try:
        # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        result = pwd_context.verify(plain_password, hashed_password)
        return result
    except Exception as e:
        logging.error(f"Error verifying password: {e}")
        return False
