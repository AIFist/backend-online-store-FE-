from pydantic import BaseModel
from datetime import datetime
class ProductSalesCreate(BaseModel):
    discount_percent: float
    product_id:int


class ProdcutSalesUpdate(BaseModel):
    discount_percent: float


class ProductSalesCreateResponse(ProductSalesCreate):
    id: int
    sale_date: datetime


class ProductSalesUpdateResponse(ProductSalesCreateResponse):
    pass