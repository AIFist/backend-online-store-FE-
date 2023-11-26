from pydantic import BaseModel

class CreateReview(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str
    
class UpdateReview(CreateReview):
    pass