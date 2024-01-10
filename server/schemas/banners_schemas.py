from pydantic import BaseModel
from server.schemas.filter_products_schemas import ProductForNewArrivalesResponse

class CreateBanner(BaseModel):
    product_id: int


class BannerCreateResponse(CreateBanner):
    id: int


class BannerGetAllResponse(ProductForNewArrivalesResponse):
    pass