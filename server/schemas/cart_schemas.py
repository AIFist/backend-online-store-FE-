from pydantic import BaseModel

class ProductCartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    
class ProductCartUpdate(BaseModel):
    quantity: int