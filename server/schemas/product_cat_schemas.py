from pydantic import BaseModel
from typing import Optional
class ProductCategoryCreate(BaseModel):
    category_name: str
    parent_category_id: Optional[int]

class ProductCategoryUpdate(ProductCategoryCreate):
    # category_name: str
    pass