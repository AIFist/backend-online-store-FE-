from pydantic import BaseModel, EmailStr,Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: EmailStr
    first_name: Optional[str] | None
    last_name: Optional[str] | None
    role: str 
    billing_address: Optional[str] | None
    shipping_address:  Optional[str] | None



class TokenData(BaseModel):
    id: Optional[str] = None