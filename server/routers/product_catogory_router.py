from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_cat_schemas
from server.db import product_cat_helper
from typing import List
from server.utils import oauth2

router = APIRouter(prefix="/product_cat", tags=["Product category CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_model=product_cat_schemas.ProductCategoryCreateResponse)
async def create_product_category(
    product_category: product_cat_schemas.ProductCategoryCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Create a new product category.

    Args:
    - product_category: ProductCategoryCreate model from product_cat_schemas containing data for the new category.

    Returns:
    - Newly created ProductCategory.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    data = product_cat_helper.helper_create_product_category(session=session, product_category=product_category)
    return data


@router.post("/createall",
             status_code=status.HTTP_201_CREATED,
             response_model=List[product_cat_schemas.ProductCategoryCreateResponse])
async def create_product(
    products_category: List[product_cat_schemas.ProductCategoryCreate] = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Create multiple product categories and return the created categories.

    Parameters:
    - products_category: A list of product categories to be created.

    Returns:
    - A list of the created product categories.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    created_categories = []
    for product_category in products_category:
        created_category = product_cat_helper.helper_create_product_category(
            session=session, product_category=product_category
        )
        created_categories.append(created_category)
    return created_categories


# Delete a product category
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_category(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Delete a product category by its ID.

    Args:
        id (int): The ID of the product category to be deleted.

    Raises:
        HTTPException: If the product category with the given ID does not exist.

    Returns:
        Response: A response with no content.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    res =product_cat_helper.helper_delete_product_category(session=session, id=id)
    return res


# Update a product category
@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED, 
            response_model= product_cat_schemas.ProductCategoryUpdateResponse,)
async def update_product_category(
    id: int,
    productcat_update: product_cat_schemas.ProductCategoryUpdate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Update a product category by ID.

    Parameters:
    - id: ID of the product category to be updated.
    - productcat_update: ProductCategoryUpdate model containing updated data.

    Returns:
    - Updated ProductCategory.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    updated_product = product_cat_helper.helper_update_product_category(session=session, id=id, productcat_update=productcat_update)
    return updated_product


# Get all product categories with their IDs and names
@router.get("/all", 
            response_model=List[product_cat_schemas.ProductCategoryGetALLResponse])
async def get_product_category():
    """
    Get all product categories with their IDs and names.

    Returns:
    List of tuples containing (category_id, category_name).
    """
    data = product_cat_helper.helper_get_product_category(session=session)
    # Create a list of tuples with category id and name
    
    # Return the result
    return data

# Get a specific product category by ID
@router.get("/{id}", response_model=product_cat_schemas.ProductCategoryGetResponse)
async def get_one_product_category(id: int):
    """
    Retrieve a specific product category by ID.

    Parameters:
    - id: The ID of the product category to retrieve.

    Returns:
    - The product category with the specified ID.

    Raises:
    - HTTPException: If the product category is not found.
    """
    data = product_cat_helper.helper_get_one_product_category(session=session, id=id)
    return data
