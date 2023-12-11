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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(id: int):
    """
    Delete a product image by its ID.

    Args:
        id (int): The ID of the product image to be deleted.

    Raises:
        HTTPException: If the product image with the given ID does not exist.
    """
    return product_image_helper.helper_delete_product_image(session=session, id=id)


@router.put("/{id}", response_model=product_image_schemas.ProductImageUpdateResponse)
async def update_product_image(id: int, product_image: product_image_schemas.ProductImageUpdate = Body(...)):
    """
    Update a product image in the database.

    Args:
        id (int): ID of the product image to update.
        product_image (ProductImageUpdate): Object containing the updated data.

    Returns:
        ProductImage: The updated product image.

    Raises:
        HTTPException: If the product image does not exist.
    """
    return product_image_helper.helper_update_product_image(session=session, id=id, product_image=product_image)