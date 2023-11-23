from pydantic import BaseModel , EmailStr
from typing import Optional

class ProductCreate(BaseModel):
    product_name: str
    description: str
    price: int
    stock_quantity: int
    product_size: str
    image_path: Optional[str]
    target_audience: str
    category_id: Optional[int]