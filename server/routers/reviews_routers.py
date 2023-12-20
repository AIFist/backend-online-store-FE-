from fastapi import Body, status, Depends
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import reviews_schemas
from server.db import review_helper
from server.utils import oauth2
from typing import List
router = APIRouter(prefix="/review", tags=["Review  CRUD"])

@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             response_model=reviews_schemas.CreateReviewResponse
             )
async def create_review(
    sub_product_data: reviews_schemas.SubCreateReview = Body(...),
    current_user: int = Depends(oauth2.get_current_user),):
    """
    Create a new review.

    Parameters:
    - product_data: Pydantic model containing review details.

    Returns:
    - Created Review.
    """
    product_data = {
        "user_id": current_user.id,
        "product_id": sub_product_data.product_id,
        "rating": sub_product_data.rating,
        "comment": sub_product_data.comment
    }
    try:
        product_data = reviews_schemas.CreateReview.model_validate(product_data)
    except ValueError as e:
        print(f"An error occurred: {e}")
    
    data = review_helper.helper_create_review(session=session, product_data=product_data)
    return data


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def review_update(id: int, review_update: reviews_schemas.UpdateReview = Body(...)):
    """
    Update a review by ID.

    Parameters:
    - id: ID of the review to be updated.
    - review_update: Pydantic model containing updated review data.

    Returns:
    - Updated Review.
    """
    data = review_helper.helper_review_update(session=session, id=id, review_update=review_update)
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int,):
    """
    Delete a Review by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
    """
    data = review_helper.helper_delete_product(session=session, id=id)
    return data


@router.get("/{id}", 
            status_code=status.HTTP_200_OK,
            response_model=List[reviews_schemas.GetAllReview]
            )
def get_all_review_of_one_product(id: int):
    """
    Get all reviews of a product based on its ID.

    Args:
        id (int): The ID of the product.

    Returns:
        List[Review]: A list of reviews for the product.

    Raises:
        HTTPException: If the product does not have any review.
    """
    data = review_helper.helper_get_all_review_of_one_product(session=session, id=id)
    return data


# TODO add review functions that send review with profduct
def review_with_product():
    pass