from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_image_schemas
from server.db import product_image_helper
from typing import List

router = APIRouter(prefix="/Product Images", tags=["Product Images CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_description="Product Image created successfully",
             response_model=product_image_schemas.ProductImageCreateResponse
             )
async def create_product_image(product_image: product_image_schemas.ProductImageCreate = Body(...)):
    """
    Create a new product image.

    Args:
    - product_image: ProductImageCreate model from product_image_schemas containing data for the new image.

    Returns:
    - Newly created ProductImage.
    """
    data = product_image_helper.helper_create_product_image(session=session, product_image=product_image)
    return data
