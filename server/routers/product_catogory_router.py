from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import product_cat_schemas
from server.db import product_cat_helper


router = APIRouter(prefix="/product_cat", tags=["Product category CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_category(product_category: product_cat_schemas.ProductCategoryCreate = Body(...)):
    """
    Create a new product category.

    Args:
    - product_category: ProductCategoryCreate model from product_cat_schemas containing data for the new category.

    Returns:
    - Newly created ProductCategory.
    """
    data = product_cat_helper.helper_create_product_category(session=session, product_category=product_category)
    return data


# Delete a product category
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_category(id: int):
    """
    Delete a product category by its ID.

    Args:
        id (int): The ID of the product category to be deleted.

    Raises:
        HTTPException: If the product category with the given ID does not exist.

    Returns:
        Response: A response with no content.
    """
    res =product_cat_helper.helper_delete_product_category(session=session, id=id)
    return res


# Update a product category
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product_category(id: int, productcat_update: product_cat_schemas.ProductCategoryUpdate = Body(...)):
    """
    Update a product category by ID.

    Parameters:
    - id: ID of the product category to be updated.
    - productcat_update: ProductCategoryUpdate model containing updated data.

    Returns:
    - Updated ProductCategory.
    """
    updated_product = product_cat_helper.helper_update_product_category(session=session, id=id, productcat_update=productcat_update)
    return updated_product


# Get all product categories with their IDs and names
@router.get("/all")
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
@router.get("/{id}")
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
