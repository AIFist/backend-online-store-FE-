from pydantic import BaseModel

class CreateBanner(BaseModel):
    product_id: int
    
class BannerCreateResponse(CreateBanner):
    id: int