from pydantic import BaseModel
from datetime import datetime
class CreateReview(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str


class UpdateReview(BaseModel):
    rating: int
    comment: str


class CreateReviewResponse(CreateReview):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# following class inherits from CreateReviewResponse becasue both returns whole object of review
class UpdateReviewResponse(CreateReviewResponse):
    pass

# following class inherits from CreateReviewResponse becasue both returns whole object of review
class GetAllReview(CreateReviewResponse):
    pass