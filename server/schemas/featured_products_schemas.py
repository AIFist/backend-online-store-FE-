from pydantic import BaseModel

class FeaturedProductCreate(BaseModel):
    product_id: int