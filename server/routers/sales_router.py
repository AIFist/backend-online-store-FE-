from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import sales_schemas
from server.db import  sales_helper

router = APIRouter(prefix="/sales", tags=["Product sales CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_model=sales_schemas.ProductSalesCreateResponse
             )
async def create_product_sales(
    product_sales: sales_schemas.ProductSalesCreate = Body(...)
):
    """
    Creates a new product sales.

    Args:
        product_sales (sales_schemas.ProductSalesCreate): The product sales data.

    Returns:
        The created product sales data.
    """

    # Create the product sales in the database
    data = sales_helper.helper_create_product_sales(
        session=session, product_sales=product_sales
    )
    return data


@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED,
            response_model=sales_schemas.ProductSalesUpdateResponse
            )
async def product_sales_update(id: int, product_sales_update: sales_schemas.ProdcutSalesUpdate = Body(...)):
    """
    Update a product sales by ID.

    Args:
    - id: ID of the product sales to be updated.
    - product_sales_update: ProductSalesUpdate model containing updated data for the product sales.

    Returns:
    - The updated product sales.
    """
    data = sales_helper.helper_update_product_sales(
        session=session, id=id, product_sales_update=product_sales_update
    )
    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_sales(id: int):
    """
    Delete a product sales by ID.

    Args:
    - id: ID of the product sales to be deleted.

    Returns:
    - The deleted product sales.
    """
    data = sales_helper.helper_delete_product_sales(session=session, id=id)
    return data
