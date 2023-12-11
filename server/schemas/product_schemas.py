from pydantic import BaseModel , EmailStr
from typing import List
from datetime import datetime

class ProductImageCreate(BaseModel):
    image_path: str


class ProductCreate(BaseModel):
    product_name: str
    description: str
    price: float
    stock_quantity: int
    product_size: str
    target_audience: str
    SKU:str
    product_color: str
    category_id: int
    images: List[ProductImageCreate]


class ProductUpadte(BaseModel):
    product_name: str
    description: str
    price: float
    stock_quantity: int
    product_size: str
    target_audience: str
    SKU:str
    product_color: str
    category_id: int
    
class CreatedProducts(BaseModel):
    products: List[ProductCreate]


class ProductCreateResponse(ProductCreate):
    id: int
    created_at: datetime
    images: List[str]
    class Config:
        from_attributes = True
 

class ProductUpadteResponse(ProductUpadte):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ProductImageGet(BaseModel):
    id: int
    image_path: str


class ProductGetResponse(ProductCreate):
    id: int
    created_at: datetime
    images: List[ProductImageGet]
    class Config:
        from_attributes = True