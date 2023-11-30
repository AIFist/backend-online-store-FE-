from pydantic import BaseModel

class ProductSalesCreate(BaseModel):
    discount_percent: float
    
class ProdcutSalesUpdate(ProductSalesCreate):
    pass
    