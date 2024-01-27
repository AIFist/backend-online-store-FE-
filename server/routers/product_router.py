from fastapi import Body, status, Depends, HTTPException, Request
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_schemas
from server.db import product_helper
from typing import List
from server.utils import oauth2
from server.utils.rate_limit import rate_limited



router = APIRouter(prefix="/product", tags=["Product  CRUD"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=product_schemas.ProductCreateResponse
)
async def create_product(
    product_data: product_schemas.ProductCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new product along with associated images.
    
    Args:
        product_data (product_schemas.ProductCreate): Pydantic model containing product details.
        current_user (int): The ID of the current user.

    Raises:
        HTTPException: If the current user does not have permission to perform this action.

    Returns:
        product_schemas.ProductCreateResponse: The created product.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    
    data = product_helper.helper_create_product(session=session, product_data=product_data)
    return data


@router.post(
    "/createall",
    status_code=status.HTTP_201_CREATED,
    response_model=List[product_schemas.ProductCreateResponse]
)
async def create_product(
    products_data: List[product_schemas.ProductCreate] = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create multiple products along with associated images.
    
    Parameters:
    - products_data: List of Pydantic models containing product details.
    - current_user: ID of the current user making the request.
    
    Returns:
    - List of created products.
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    
    # Create a list to store the created products
    return_list = []
    
    # Iterate over each product data to create the product
    for product_data in products_data:
        # Use a helper function to create the product and add it to the list
        data = product_helper.helper_create_product(session=session, product_data=product_data)
        return_list.append(data)
    
    # Return the list of created products
    return return_list


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
    - HTTPException: If the current user does not have permission to perform this action.

    Returns:
    - Response with 204 status code if successful.
    """
    # Check if the current user is an admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

    # Delete the product
    res = product_helper.helper_for_deleting_product(session=session, id=id)
    return res


# Update a product 
@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED,
            response_model=product_schemas.ProductUpadteResponse
            )
async def update_product(
    id: int,  # ID of the product to be updated.
    product_update: product_schemas.ProductUpadte = Body(...),  # Pydantic model containing updated data.
    current_user: int = Depends(oauth2.get_current_user),  # Get the current user from OAuth2.

    ):
    """
    Update a product by ID.

    Parameters:
    - id: ID of the product to be updated.
    - product_update: Pydantic model containing updated data.
    - current_user: ID of the current user.

    Returns:
    - Updated Product.
    """
    if current_user.role != "admin":  # Check if the current user is an admin.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    updated_product = product_helper.helper_update_product(session=session, id=id, product_update=product_update)  # Update the product using the helper function.
    return updated_product  # Return the updated product.


@router.get("/{product_id}", 
            status_code=status.HTTP_200_OK,
            response_model=product_schemas.ProductGetResponseAdvance
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_one_product(request: Request,product_id: int):
    """
    Get a single product with its images based on the provided product ID.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Get the product with the given id but image it gets one image at a time and this issue needs to be fixed
    query= product_helper.get_product_by_id(product_id=product_id)
    results = session.execute(query).first()
    return results
    
