from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import featured_products_schemas
from server.db import    featured_helper

router = APIRouter(prefix="/featured", tags=["featured Product CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_featured_product(
    featured_product: featured_products_schemas.FeaturedProductCreate = Body(...)
):
    """
    Creates a new featured product.

    Args:
        featured_product (featured_products_schemas.FeaturedProductCreate): The featured product data.

    Returns:
        The created featured product data.
    """

    # Create the featured product in the database
    data = featured_helper.helper_create_featured_product(
        session=session, featured_product=featured_product
    )
    return data

@router.delete("/delete/{featured_product_id}")
async def delete_featured_product(featured_product_id: int):
    """
    Deletes a featured product.

    Args:
        featured_product_id (int): The ID of the featured product to delete.

    Returns:
        None
    """

    # Delete the featured product from the database
    res = featured_helper.helper_delete_featured_product(
        session=session, featured_product_id=featured_product_id
    )
    return res