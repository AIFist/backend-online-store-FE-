from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_schemas
from server.db import product_helper
router = APIRouter(prefix="/product", tags=["Product  CRUD"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: product_schemas.ProductCreate = Body(...)):
    """
    Create a new product along with associated images.
    
    Parameters:
    - product_data: Pydantic model containing product details.
    
    Returns:
    - Created Product.
    """
    
    data = product_helper.helper_create_product(session=session, product_data=product_data)
    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
    """
    res = product_helper.helper_for_deleting_product(session=session, id=id)
    return res


# Update a product 
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product(id: int, product_update: product_schemas.ProductUpadte = Body(...)):
    """
    Update a product by ID.

    Parameters:
    - id: ID of the product to be updated.
    - product_update: Pydantic model containing updated data.

    Returns:
    - Updated Product.
    """
    updated_product = product_helper.helper_update_product(session=session, id=id, product_update=product_update)
    return updated_product


@router.get("/{id}")
async def get_one_product(id: int):
    """
    Get a single product with its images based on the provided product ID.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Get the product with the given id but image it gets one image at a time and this issue needs to be fixed
    data = product_helper.helper_for_get_one_product(session= session, id=id)
    return data
    
