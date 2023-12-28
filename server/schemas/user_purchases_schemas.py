from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from server.schemas.product_schemas import ProductCreateResponse,ProductImageCreate

class SubUserPurchasesCreate(BaseModel):
    product_id: int
    status: str = Field(default="pending")


class UserPurchasesCreate(SubUserPurchasesCreate):
    user_id: int
    


class  UserPurchasesUpdate(BaseModel):
    status: str


class UserPurchasesCreateResponse(SubUserPurchasesCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
 
 
class UserPurchasesUpdateResponse(UserPurchasesCreateResponse):
    pass

# this class inherite from ProductImageCreate class for image data
class ProductImage(ProductImageCreate):
    id: int
    product_id : int


# this class inherite from ProductCreateResponse  class for product data

class Product(ProductCreateResponse):
    images: List[ProductImage]

# this class inherite from UserPurchasesCreateResponse  class for user purchase data
class UserPurchasesGetAll(UserPurchasesCreateResponse):
    product: Product
    class Config:
        from_attributes = True
 
