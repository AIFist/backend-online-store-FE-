from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class ProductCategoryCreate(BaseModel):
    category_name: str
    parent_category_id: Optional[int]

class ProductCategoryUpdate(ProductCategoryCreate):
    # category_name: str
    pass

class ProductCategoryCreateResponse(ProductCategoryCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class ProductCategoryUpdateResponse(ProductCategoryCreateResponse):
    pass


class ProductCategoryGetResponse(ProductCategoryCreateResponse):
    pass

class ProductCategoryGetALLResponse(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True