# from pydantic import BaseModel
from server.schemas.product_schemas import ProductCreateResponse,ProductImageCreate
from typing import List, Optional

class LandingPageProductImage(ProductImageCreate):
    id: int

class LandingPageProductCResponse(ProductCreateResponse):
    images: List[LandingPageProductImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    avg_discount_percent: Optional[float] | None
    

