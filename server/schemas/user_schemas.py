from pydantic import BaseModel , EmailStr,Field
from typing import Optional

class GetUser(BaseModel):
    """   This schema is for reciving user data  """
    username: str
    email :EmailStr
    password: str
    role:str =Field(default="user")
    billing_address: Optional[str] | None
    shipping_address:  Optional[str] | None


class AuthUser(BaseModel):
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    email : EmailStr
    username : str
    billing_address: Optional[str] | None
    shipping_address: Optional[str] | None
