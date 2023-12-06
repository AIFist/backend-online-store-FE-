from server.schemas import featured_products_schemas
from sqlalchemy.exc import SQLAlchemyError
from server.models.models import FeaturedProduct, Product, ProductImage
from fastapi import status,HTTPException, Response


def helper_create_featured_product(session, featured_product: featured_products_schemas.FeaturedProductCreate):
    """
    Creates a new featured product.

    Args:
        session: The database session.
        featured_product: The featured product data.

    Returns:
        The created featured product data.
    """
    try:
        # Create a new FeaturedProduct instance using the data from the featured_product model
        new_featured_product = FeaturedProduct(**featured_product.model_dump())

        # Add the new_featured_product to the session
        session.add(new_featured_product)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_featured_product with the latest data from the database
        session.refresh(new_featured_product)

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

    # Return the newly created featured product
    return new_featured_product
    

def helper_delete_featured_product(session, featured_product_id:int):
    """
    Delete a featured product with the given ID.

    Args:
        session (Session): SQLAlchemy session object.
        featured_product_id (int): ID of the featured product to delete.

    Returns:
        Response: FastAPI response with status code 204 if successful.

    Raises:
        HTTPException: If the product with the given ID does not exist.
    """
    try:
        # Query the product with the given id
        featured_product_query = session.query(FeaturedProduct).filter(FeaturedProduct.id == featured_product_id)
        featured_product = featured_product_query.first()

        # If product does not exist, raise 404 error
        if featured_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {featured_product_id} does not exist")

        # Delete the product
        featured_product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)