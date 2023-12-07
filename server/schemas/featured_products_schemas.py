from pydantic import BaseModel
from datetime import datetime


class FeaturedProductCreate(BaseModel):
    product_id: int

class FeaturedProductCreateResponse(FeaturedProductCreate):
    id: int
    created_at: datetime