from fastapi import Body, status,Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import favorites_schemas
from server.db import  favorites_helper
from server.utils import oauth2
from typing import List
from server.models.models import Favorite as Favorites
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/favorites", tags=["Product favorite CRUD"])
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=favorites_schemas.ProductFavoriteCreateResponse
)
async def create_product_favorite(
    sub_product_favorite: favorites_schemas.ProductFavoriteSubCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new product favorite.

    Args:
        sub_product_favorite (favorites_schemas.ProductFavoriteSubCreate): The data for creating a product favorite.
        current_user (int): The ID of the current user.

    Returns:
        favorites_schemas.ProductFavoriteCreateResponse: The created product favorite data.

    Raises:
        HTTPException: If the current user is not authorized to perform the requested action.
    """
    # Prepare the data for creating the product favorite
    update_data = {
        "user_id": current_user.id,
        "product_id": sub_product_favorite.product_id
    }

    try:
        # Validate the data for creating the product favorite
        product_favorite = favorites_schemas.ProductFavoriteCreate.model_validate(update_data)
    except ValueError as e:
        print(f"An error occurred: {e}")
        
    # Create the product favorite in the database
    data = favorites_helper.helper_create_product_favorite(
        session=session, product_favorite=product_favorite
    )

    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_favorite(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a product favorite by ID.

    Args:
        id (int): ID of the product favorite to be deleted.
        current_user (int, optional): ID of the current user. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: If the current user is not authorized to perform the requested action.

    Returns:
        dict: The deleted product favorite.
    """
    try:
        # Query the favorite product by ID
        favorite_product_query = session.query(Favorites).filter(Favorites.id == id)
        product_favorite = favorite_product_query.first()
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")
        
        # Rollback the transaction
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while deleting product favorite",
        )

    # Check if the current user is authorized to delete the favorite product
    if current_user.id != product_favorite.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
        
    # Delete the product favorite and return the result
    data = favorites_helper.helper_delete_product_favorite(session=session, id=id)
    return data

@router.get("/get-all",status_code=status.HTTP_200_OK,
            response_model=List[favorites_schemas.ProductFavoriteGetAll]
            )
async def get_all_product_favorite(current_user: int = Depends(oauth2.get_current_user)):
    """
    Get all product favorites for the current user.
    
    Args:
        current_user (int): The ID of the current user.
        
    Returns:
        List[favorites_schemas.ProductFavoriteGetAll]: A list of product favorites.
    """
    UserId = current_user.id
    data = favorites_helper.helper_get_all_product_favorite(session=session,UserId=UserId)
    return data