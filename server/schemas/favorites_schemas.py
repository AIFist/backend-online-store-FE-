from pydantic import BaseModel

class ProductFavoriteCreate(BaseModel):
    product_id: int
    user_id: int