from pydantic import BaseModel , EmailStr
from typing import List

class ProductImageCreate(BaseModel):
    image_path: str

class ProductCreate(BaseModel):
    product_name: str
    description: str
    price: int
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
    price: int
    stock_quantity: int
    product_size: str
    target_audience: str
    SKU:str
    product_color: str
    category_id: int
    
class CreatedProducts(BaseModel):
    products: List[ProductCreate]
    
