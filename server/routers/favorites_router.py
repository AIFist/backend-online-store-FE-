from fastapi import Body, status,Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import favorites_schemas
from server.db import  favorites_helper
from server.utils import oauth2
from typing import List
router = APIRouter(prefix="/favorites", tags=["Product favorite CRUD"])

@router.post("/create",
             status_code=status.HTTP_201_CREATED,
             response_model=favorites_schemas.ProductFavoriteCreateResponse
             )
async def create_product_favorite(
    product_favorite: favorites_schemas.ProductFavoriteCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new product favorite.

    Args:
        product_favorite (favorites_schemas.ProductFavoriteCreate): The product favorite data.

    Returns:
        The created product favorite data.
    """
    print(current_user.id, current_user.role)
    if current_user.id != product_favorite.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # Create the product favorite in the database
    data = favorites_helper.helper_create_product_favorite(
        session=session, product_favorite=product_favorite
    )
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_favorite(id: int):
    """
    Delete a product favorite by ID.

    Args:
    - id: ID of the product favorite to be deleted.

    Returns:
    - The deleted product favorite.
    """
    data = favorites_helper.helper_delete_product_favorite(session=session, id=id)
    return data

@router.get("/{UserId}",status_code=status.HTTP_200_OK,
            response_model=List[favorites_schemas.ProductFavoriteGetAll]
            )
async def get_all_product_favorite(UserId: int):
    """
    Get all product favorites.

    Returns:
    - A list of product favorites.
    """
    data = favorites_helper.helper_get_all_product_favorite(session=session,UserId=UserId)
    return data