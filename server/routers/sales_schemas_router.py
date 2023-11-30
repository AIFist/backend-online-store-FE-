from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import sales_schemas
from server.db import  sales_helper

router = APIRouter(prefix="/sales", tags=["Product sales CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
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
