from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_schemas
from server.db import product_helper
from typing import List
from server.utils import oauth2
router = APIRouter(prefix="/product", tags=["Product  CRUD"])


@router.post("/create",
             status_code=status.HTTP_201_CREATED, 
             response_model=product_schemas.ProductCreateResponse
             )
async def create_product(
    product_data: product_schemas.ProductCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Create a new product along with associated images.
    
    Parameters:
    - product_data: Pydantic model containing product details.
    
    Returns:
    - Created Product.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    
    data = product_helper.helper_create_product(session=session, product_data=product_data)
    return data


@router.post("/createall", 
             status_code=status.HTTP_201_CREATED,
             response_model=List[product_schemas.ProductCreateResponse])
async def create_product(
    products_data: List[product_schemas.ProductCreate] = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Create a new product along with associated images.
    
    Parameters:
    - product_data: Pydantic model containing product details.
    
    Returns:
    - Created Product.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return_list = []
    for product_data in products_data:
        data = product_helper.helper_create_product(session=session, product_data=product_data)
        return_list.append(data)
    return return_list


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    res = product_helper.helper_for_deleting_product(session=session, id=id)
    return res


# Update a product 
@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED,
            response_model=product_schemas.ProductUpadteResponse
            )
async def update_product(
    id: int,
    product_update: product_schemas.ProductUpadte = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Update a product by ID.

    Parameters:
    - id: ID of the product to be updated.
    - product_update: Pydantic model containing updated data.

    Returns:
    - Updated Product.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    updated_product = product_helper.helper_update_product(session=session, id=id, product_update=product_update)
    return updated_product


@router.get("/{product_id}", 
            status_code=status.HTTP_200_OK,
            response_model=product_schemas.ProductGetResponseAdvance
            )
async def get_one_product(product_id: int):
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
    
