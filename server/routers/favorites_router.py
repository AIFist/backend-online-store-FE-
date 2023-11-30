from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import favorites_schemas
from server.db import  favorites_helper

router = APIRouter(prefix="/favorites", tags=["Product favorite CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_favorite(
    product_favorite: favorites_schemas.ProductFavoriteCreate = Body(...)
):
    """
    Creates a new product favorite.

    Args:
        product_favorite (favorites_schemas.ProductFavoriteCreate): The product favorite data.

    Returns:
        The created product favorite data.
    """

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