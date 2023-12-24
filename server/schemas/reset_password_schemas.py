from pydantic import BaseModel, EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordResponse(BaseModel):
    message: str
    
class ResetPassword(BaseModel):
    token: str
    new_password: str
    