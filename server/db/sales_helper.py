from fastapi import status,HTTPException, Response
from server.models.models import Sales
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import sales_schemas
from sqlalchemy.orm import joinedload

def helper_create_product_sales(session ,product_sales: sales_schemas.ProductSalesCreate):
    """
    Create a new product sales.

    Args:
    - product_sales: ProductSalesCreate model containing data for the new product sales.

    Returns:
    - The newly created product sales.
    """
    try:
        # Create a new ProductSales instance using the data from the product_sales model
        new_product_sales = Sales(**product_sales.model_dump())

        # Add the new_product_sales to the session
        session.add(new_product_sales)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_sales with the latest data from the database
        session.refresh(new_product_sales)

    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
    finally:
        # Close the session
        session.close()
    
    # Return the newly created product cart
    return new_product_sales