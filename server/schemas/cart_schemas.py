from pydantic import BaseModel
from datetime import datetime

class ProductCartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    
class ProductCartUpdate(BaseModel):
    quantity: int
    
class ProductCartCreateResponse(ProductCartCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ProductCartUpdateResponse(ProductCartCreateResponse):
    pass

class ProductCartGetResponse(ProductCartCreateResponse):
    pass