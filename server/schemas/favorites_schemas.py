from pydantic import BaseModel
from datetime import datetime
from typing import List
from server.schemas.product_schemas import ProductCreateResponse,ProductImageCreate


class ProductFavoriteSubCreate(BaseModel):
    product_id: int


class ProductFavoriteCreate(ProductFavoriteSubCreate):
    user_id: int


class ProductFavoriteCreateResponse(ProductFavoriteSubCreate):
    id : int
    created_at: datetime

# this class inherite from ProductImageCreate class for image data
class ProductImage(ProductImageCreate):
    id: int
    product_id : int


# this class inherite from ProductCreateResponse  class for product data

class Product(ProductCreateResponse):
    images: List[ProductImage]

# this class inherite from ProductCreateResponse  class for ProductFavorite data
class ProductFavoriteGetAll(ProductFavoriteCreateResponse):
    product: Product
    class Config:
        from_attributes = True
 
