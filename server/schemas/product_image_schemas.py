from pydantic import BaseModel

class ProductImageCreate(BaseModel):
    image_path: str
    product_id : int
    

class ProductImageCreateResponse(ProductImageCreate):
    id: int