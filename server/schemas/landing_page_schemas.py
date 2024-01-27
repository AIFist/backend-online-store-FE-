from pydantic import BaseModel
from server.schemas.product_schemas import ProductCreateResponse,ProductImageCreate
# from server.schemas.filter_products_schemas import FeaturedProductUpToGivenNumberResponse
from server.schemas.product_schemas import ProductUpadte
from typing import List, Optional
from datetime import datetime


class LandingPageProductImage(ProductImageCreate):
    id: int

class LandingPageProductCResponse(ProductCreateResponse):
    images: List[LandingPageProductImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    discount_percent: Optional[float] | None
    category_name: str
    
class LandingPageUpToGivenNumberImageResponse(LandingPageProductImage):
    product_id : int


class ProductRespose(ProductUpadte):
    id:int
    created_at:datetime
class LandingPageUpToGivenNumberResponse(BaseModel):
    Product : ProductRespose
    ProductImage: LandingPageUpToGivenNumberImageResponse
    num_reviews: int
    avg_rating: Optional[float] | None
    discount_percent: Optional[float] | None
    purchase_count: Optional[int]| None
    category_name: str

