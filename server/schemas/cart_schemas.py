from pydantic import BaseModel
from datetime import datetime
from server.schemas.product_schemas import ProductCreate, ProductImageGet
from typing import List

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

class ProductCartGetResponseImage(ProductImageGet):
    product_id:int


class ProductCartGetResponseProduct(ProductCreate):
     images: List[ProductCartGetResponseImage]



class ProductCartGetResponse(ProductCartCreateResponse):
    product : ProductCartGetResponseProduct