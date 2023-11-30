from pydantic import BaseModel

class ProductSalesCreate(BaseModel):
    discount_percent: float