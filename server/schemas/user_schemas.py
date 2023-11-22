from pydantic import BaseModel , EmailStr


class GetUser(BaseModel):
    """   This schema is for reciving user data  """
    username: str
    email :EmailStr
    password: str


class AuthUser(BaseModel):
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    email : EmailStr
    username : str
