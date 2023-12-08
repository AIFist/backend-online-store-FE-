# from pydantic import BaseModel
from server.schemas.product_schemas import ProductCreateResponse,ProductImageCreate
from typing import List, Optional

class FilterProductsProductImage(ProductImageCreate):
    id: int

class FilterProductsProductCResponse(ProductCreateResponse):
    images: List[FilterProductsProductImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    avg_discount_percent: Optional[float] | None
    

