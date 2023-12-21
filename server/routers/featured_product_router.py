from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import featured_products_schemas
from server.db import featured_helper
from server.utils import oauth2
router = APIRouter(prefix="/featured", tags=["featured Product CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_model=featured_products_schemas.FeaturedProductCreateResponse
             )
async def create_featured_product(
    featured_product: featured_products_schemas.FeaturedProductCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new featured product.

    Args:
        featured_product (featured_products_schemas.FeaturedProductCreate): The featured product data.

    Returns:
        The created featured product data.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    
    # Create the featured product in the database
    data = featured_helper.helper_create_featured_product(
        session=session, featured_product=featured_product
    )
    return data

@router.delete("/delete/{featured_product_id}")
async def delete_featured_product(
    featured_product_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Deletes a featured product.

    Args:
        featured_product_id (int): The ID of the featured product to delete.

    Returns:
        None
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    # Delete the featured product from the database
    res = featured_helper.helper_delete_featured_product(
        session=session, featured_product_id=featured_product_id
    )
    return res