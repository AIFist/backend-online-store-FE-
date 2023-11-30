from pydantic import BaseModel, Field
class UserPurchasesCreate(BaseModel):
    user_id: int
    product_id: int
    status: str = Field(default="pending")

class  UserPurchasesUpdate(BaseModel):
    status: str