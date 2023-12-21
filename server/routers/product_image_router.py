from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_image_schemas
from server.db import product_image_helper
from server.utils import oauth2

router = APIRouter(prefix="/Product Images", tags=["Product Images CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_description="Product Image created successfully",
             response_model=product_image_schemas.ProductImageCreateResponse
             )
async def create_product_image(
    product_image: product_image_schemas.ProductImageCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Create a new product image.

    Args:
    - product_image: ProductImageCreate model from product_image_schemas containing data for the new image.

    Returns:
    - Newly created ProductImage.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    data = product_image_helper.helper_create_product_image(session=session, product_image=product_image)
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(
    id: int,
    current_id = Depends(oauth2.get_current_user),
    ):
    """
    Delete a product image by its ID.

    Args:
        id (int): The ID of the product image to be deleted.

    Raises:
        HTTPException: If the product image with the given ID does not exist.
    """
    if current_id.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return product_image_helper.helper_delete_product_image(session=session, id=id)


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            response_model=product_image_schemas.ProductImageUpdateResponse)
async def update_product_image(
    id: int,
    product_image: product_image_schemas.ProductImageUpdate = Body(...),
    current_id = Depends(oauth2.get_current_user),
    ):
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
    if current_id.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return product_image_helper.helper_update_product_image(session=session, id=id, product_image=product_image)