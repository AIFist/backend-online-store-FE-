from pydantic import BaseModel

class ProductImageCreate(BaseModel):
    image_path: str
    product_id : int
    

class ProductImageCreateResponse(ProductImageCreate):
    id: int
    
class ProductImageUpdate(ProductImageCreate):
    pass

class ProductImageUpdateResponse(ProductImageCreateResponse):
    pass