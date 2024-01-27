from fastapi import Body, status, Depends, HTTPException, Request
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_cat_schemas
from server.db import product_cat_helper
from typing import List
from server.utils import oauth2
from server.utils.rate_limit import rate_limited


router = APIRouter(prefix="/product_cat", tags=["----------------------Required Admin Role------------------------ Product category CRUD"])

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=product_cat_schemas.ProductCategoryCreateResponse,
)
async def create_product_category(
    product_category: product_cat_schemas.ProductCategoryCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new product category.

    Args:
        product_category (ProductCategoryCreate): Data for the new category.
        current_user (int): ID of the current user.

    Returns:
        ProductCategoryCreateResponse: Newly created ProductCategory.
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    # Create the product category using the helper function
    data = product_cat_helper.helper_create_product_category(
        session=session, product_category=product_category
    )
    return data


@router.post(
    "/createall",
    status_code=status.HTTP_201_CREATED,
    response_model=List[product_cat_schemas.ProductCategoryCreateResponse],
)
async def create_product(
    products_category: List[product_cat_schemas.ProductCategoryCreate] = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create multiple product categories and return the created categories.

    Args:
        products_category (List[product_cat_schemas.ProductCategoryCreate]):
            A list of product categories to be created.

        current_user (int): The ID of the current user making the request.

    Raises:
        HTTPException: If the current user does not have admin role.

    Returns:
        List[product_cat_schemas.ProductCategoryCreateResponse]:
            A list of the created product categories.
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    
    created_categories = []
    
    # Create each product category and add it to the list of created categories
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
        current_user (int): The ID of the current user.

    Raises:
        HTTPException: If the product category with the given ID does not exist.
        HTTPException: If the current user does not have permission to perform this action.

    Returns:
        Response: A response with no content.
    """

    # Check if the current user has admin role
    if current_user.role != "admin":
        # Raise an exception with the appropriate status code and detail message
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

    # Delete the product category using the helper function
    res = product_cat_helper.helper_delete_product_category(session=session, id=id)
    
    return res


# Update a product category
@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED, 
            response_model=product_cat_schemas.ProductCategoryUpdateResponse)
async def update_product_category(
    id: int,
    productcat_update: product_cat_schemas.ProductCategoryUpdate = Body(...),
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Update a product category by ID.

    Args:
        id (int): ID of the product category to be updated.
        productcat_update (ProductCategoryUpdate): ProductCategoryUpdate model containing updated data.
        current_user (int): ID of the current user.

    Returns:
        ProductCategory: Updated ProductCategory.

    Raises:
        HTTPException: If the current user does not have permission to perform this action.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    updated_product = product_cat_helper.helper_update_product_category(
        session=session,
        id=id,
        productcat_update=productcat_update
    )
    return updated_product


# Get all product categories with their IDs and names
@router.get("/all", 
            response_model=List[product_cat_schemas.ProductCategoryGetALLResponse])
@rate_limited(max_calls=10, time_frame=60)
async def get_product_category(request: Request):
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
@rate_limited(max_calls=10, time_frame=60)
async def get_one_product_category(request: Request,id: int):
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


@router.get("/",
            response_model=list[product_cat_schemas.ProductCategoryWithSubCat]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_category_all(request: Request):
    """
    Get all product categories with their sub-categories.

    Returns:
        list[product_cat_schemas.ProductCategoryWithSubCat]: A list of product categories with their sub-categories.
    """
    
    data = product_cat_helper.helper_get_all_subcategories(session=session)
    return data