from server.models.models import ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_image_schemas
from fastapi import status,HTTPException, Response

def helper_create_product_image(session, product_image:product_image_schemas.ProductImageCreate ):
    try:
        # Create a new ProductCategory instance using the data from the product_category model
        new_product_image = ProductImage(**product_image.model_dump())

        # Add the new_product_category to the session
        session.add(new_product_image)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_category with the latest data from the database
        session.refresh(new_product_image)
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably product with id {product_image.product_id} does not exist."
        )

    finally:
        # Close the session
        session.close()
    
    # Return the newly created ProductCategory
    return new_product_image


def helper_delete_product_image(session, id: int):
    """
    Deletes a product category by ID.

    Args:
        session: The database session.
        id: The ID of the product category to delete.

    Raises:
        HTTPException: If the product category does not exist.

    Returns:
        Response: A response with no content.
    """
    # Query the product category by ID
    product_image_query = session.query(ProductImage).filter(ProductImage.id == id)
    product_cat = product_image_query.first()

    # Check if the product category exists
    if product_cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} does not exist")

    # Delete the product category
    product_image_query.delete(synchronize_session=False)
    session.commit()

    # Return a response with no content
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def helper_update_product_image(session, id: int, product_image:product_image_schemas.ProductImageUpdate ):
    """
    Updates a product image by ID.

    Args:
        session: The database session.
        id: The ID of the product image to update.
        product_image: The updated product image data.

    Raises:
        HTTPException: If the product image does not exist.

    Returns:
        The updated ProductImage instance.
    """
    try:
        # Query the review by ID
        product_image_query = session.query(ProductImage).filter(ProductImage.id == id)

        # Get the review object
        product_image = product_image_query.first()

        # If the review does not exist, raise a 404 error
        if product_image is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with id {id} does not exist")

        # Update the review with the new data
        product_image_query.update(product_image.model_dump(), synchronize_session=False)

        # Commit the changes to the database
        session.commit()

    except SQLAlchemyError as e:
        # Handle any database errors and rollback the session
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably product with id {product_image.product_id} does not exist."
        )
        

    finally:
        # Close the session
        session.close()

    # Return the updated review
    return product_image_query.first()
