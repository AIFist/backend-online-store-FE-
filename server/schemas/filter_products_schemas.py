from pydantic import BaseModel
from server.schemas.product_schemas import (
    ProductCreateResponse, #need for inhertance for FilterProductsProductCResponse
    ProductImageCreate,  # need for inhertance for FilterProductsProductImage
    ProductUpadte # need for used as type in FeaturedProductUpToGivenNumberResponse
    )
from typing import List, Optional
from datetime import datetime

class FilterProductsProductImage(ProductImageCreate):
    id: int


class FilterProductsProductCResponse(ProductCreateResponse):
    images: List[FilterProductsProductImage]
    num_reviews: int
    avg_rating: Optional[float] | None
    discount_percent: Optional[float] | None
    category_name: str
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
    category_name: str
    class Config:
        from_attributes = True


# New Arrivales 

class ProudctForNewArrivales(ProductUpadte):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class ProductForNewArrivalesResponse(BaseModel):
    Product: ProudctForNewArrivales
    ProductImage: FilterProductsProductImage
    num_reviews: int
    avg_rating: Optional[float] | None
    latest_discount_percent: Optional[float] | None
    category_name: str
    class Config:
        from_attributes = True