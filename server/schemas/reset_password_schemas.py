from pydantic import BaseModel, EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr

    
class ResetPassword(BaseModel):
    token: str
    new_password: str
    