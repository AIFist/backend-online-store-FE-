from pydantic import BaseModel
from server.schemas.product_schemas import (
    ProductCreateResponse, #need for inhertance for FilterProductsProductCResponse
    ProductImageCreate,  # need for inhertance for FilterProductsProductImage
    ProductUpadte # need for used as type in FeaturedProductUpToGivenNumberResponse
    )
from typing import List, Optional


class FilterProductsProductImage(ProductImageCreate):
    id: int


class FilterProductsProductCResponse(ProductCreateResponse):
    images: List[FilterProductsProductImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    discount_percent: Optional[float] | None
    class Config:
        from_attributes = True


class FeaturedProductUpToGivenNumberImage(FilterProductsProductImage):
    product_id : int


class FeaturedProductUpToGivenNumberResponse(BaseModel):
    Product : ProductUpadte
    ProductImages: List[FeaturedProductUpToGivenNumberImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    discount_percent: Optional[float] | None
    class Config:
        from_attributes = True

