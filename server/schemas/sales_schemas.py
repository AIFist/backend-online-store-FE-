from pydantic import BaseModel

class ProductSalesCreate(BaseModel):
    discount_percent: float
    product_id:int
    
class ProdcutSalesUpdate(BaseModel):
    discount_percent: float
