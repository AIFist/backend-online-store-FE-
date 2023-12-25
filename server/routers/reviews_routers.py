from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import reviews_schemas
from server.db import review_helper
from server.utils import oauth2
from typing import List
from server.models.models import Review
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/review", tags=["Review  CRUD"])

@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             response_model=reviews_schemas.CreateReviewResponse
             )
async def create_review(
    sub_product_data: reviews_schemas.SubCreateReview = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new review.

    Parameters:
    - sub_product_data: Pydantic model containing the review details.
    - current_user: The ID of the current user.

    Returns:
    - The created review.
    """
    # Create a dictionary with the review data
    product_data = {
        "user_id": current_user.id,
        "product_id": sub_product_data.product_id,
        "rating": sub_product_data.rating,
        "comment": sub_product_data.comment
    }
    
    try:
        # Validate the review data using the Pydantic model
        product_data = reviews_schemas.CreateReview.model_validate(product_data)
    except ValueError as e:
        print(f"An error occurred: {e}")
    
    # Create the review using the helper function
    data = review_helper.helper_create_review(session=session, product_data=product_data)
    return data


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def review_update(
    id: int, 
    review_update: reviews_schemas.UpdateReview = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Update a review by ID.

    Parameters:
    - id: ID of the review to be updated.
    - review_update: Pydantic model containing updated review data.

    Returns:
    - Updated Review.
    """
    try:
        # Query the review to be updated
        review_product_query = session.query(Review).filter(Review.id == id)
        product_review = review_product_query.first()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably review with id {id} does not exist or user with id {current_user.id} does not exist."
            
        )

    # Check if the current user is authorized to update the review
    if current_user.id != product_review.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    
    # Update the review
    data = review_helper.helper_review_update(session=session, id=id, review_update=review_update)
    
    # Return the updated review
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.
    - current_user: ID of the current user.

    Raises:
    - HTTPException 403 if the current user is not authorized to delete the product.

    Returns:
    - Response with 204 status code if successful.
    """
    try:
        # Get the product review with the given ID
        product_review = session.query(Review).filter(Review.id == id).first()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably review with id {id} does not exist or user with id {current_user.id} does not exist."
        )

    # Check if the current user is authorized to delete the product review
    if current_user.id != product_review.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # Delete the product using a helper function
    data = review_helper.helper_delete_product(session=session, id=id)
    return data

# I do not think that this endpoint need authorization
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