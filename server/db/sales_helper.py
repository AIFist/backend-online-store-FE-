from fastapi import status,HTTPException, Response
from server.models.models import Sales
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import sales_schemas



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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
    )
    finally:
        # Close the session
        session.close()
    
    # Return the newly created product cart
    return new_product_sales

def helper_update_product_sales(session, id: int, product_sales_update: sales_schemas.ProdcutSalesUpdate):
    """
    Update a product sales by ID.

    Args:
    - id: ID of the product sales to be updated.
    - product_sales_update: ProductSalesUpdate model containing updated data for the product sales.

    Returns:
    - The updated product sales.
    """
    try:
        # Get the product sales from the database
        product_sales = session.query(Sales).filter(Sales.id == id).first()

        # Update the product sales with the data from the product_sales_update model
        product_sales.discount_percent = product_sales_update.discount_percent

        # Commit the changes to the database
        session.commit()

        # Refresh the product sales with the latest data from the database
        session.refresh(product_sales)

    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )
    finally:
        # Close the session
        session.close()

    # Return the updated product sales
    return product_sales

def helper_delete_product_sales(session, id: int):
    """
    Delete a product sales by ID.

    Args:
    - id: ID of the product sales to be deleted.

    Returns:
    - The deleted product sales.
    """
    try:
        # Get the product sales from the database
        product_sales = session.query(Sales).filter(Sales.id == id).first()

        # Delete the product sales
        session.delete(product_sales)

        # Commit the changes to the database
        session.commit()

    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()

    finally:
        # Close the session
        session.close()

    # Return the deleted product sales
    return Response(status_code=status.HTTP_204_NO_CONTENT)