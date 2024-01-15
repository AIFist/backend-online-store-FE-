from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import sales_schemas
from server.db import  sales_helper
from server.utils import oauth2


router = APIRouter(prefix="/sales", tags=["Product sales CRUD"])

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=sales_schemas.ProductSalesCreateResponse,
)
async def create_product_sales(
    product_sales: sales_schemas.ProductSalesCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new product sales.

    Args:
        product_sales (sales_schemas.ProductSalesCreate): The product sales data.
        current_user (int): The ID of the current user.

    Returns:
        The created product sales data.

    Raises:
        HTTPException: If the current user does not have admin role.
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
        
    # Create the product sales in the database
    data = sales_helper.helper_create_product_sales(
        session=session, product_sales=product_sales
    )
    return data


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=sales_schemas.ProductSalesUpdateResponse,
)
async def product_sales_update(
    id: int,
    product_sales_update: sales_schemas.ProdcutSalesUpdate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Update a product sales by ID.

    Args:
        - id: ID of the product sales to be updated.
        - product_sales_update: ProductSalesUpdate model containing updated data for the product sales.

    Returns:
        The updated product sales.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

    data = sales_helper.helper_update_product_sales(
        session=session, id=id, product_sales_update=product_sales_update
    )

    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_sales(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete product sales by ID.

    Parameters:
        id (int): The ID of the product sales to be deleted.
        current_user (int, optional): The ID of the current user. Defaults to None.

    Returns:
        Any: The deleted product sales data.

    Raises:
        HTTPException: If the current user does not have admin role.

    """ 
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    
    # Delete the product sales by ID
    data = sales_helper.helper_delete_product_sales(session=session, id=id)
    
    # Return the deleted product sales
    return data
