from fastapi import  status,HTTPException, Response
from server.models.models import Review
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import reviews_schemas



def helper_create_review(session, product_data: reviews_schemas.CreateReview ):
    """
    Helper function to create a review in the database.

    Args:
        session: SQLAlchemy session object.
        product_data: Instance of CreateReview class from reviews_schemas module.

    Returns:
        db_review: Instance of Review class representing the newly created review.
    """
    try:
        # Create a Review object using the product_data
        db_review = Review(**product_data.model_dump())
        
        # Add the Review object to the session
        session.add(db_review)
        
        # Commit the transaction to persist the changes
        session.commit()
        
        # Refresh the Review object to get the updated values from the database
        session.refresh(db_review)
    except SQLAlchemyError as e:
        # If an error occurs, rollback the transaction and raise an HTTPException
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. \n most probably product with id {db_review.product_id} does not exist or user with id {db_review.user_id} does not exist."
        )
    finally:
        # Close the session
        session.close()

    return db_review

 
def helper_review_update(session, id:int , review_update: reviews_schemas.UpdateReview ):
    """
    Update a review in the database.

    Args:
        session: The database session.
        id (int): The ID of the review to update.
        review_update (reviews_schemas.UpdateReview): The updated review data.

    Returns:
        Review: The updated review object.
    """
    try:
        # Query the review by ID
        review_query = session.query(Review).filter(Review.id == id)

        # Get the review object
        review = review_query.first()

        # If the review does not exist, raise a 404 error
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with id {id} does not exist")

        # Update the review with the new data
        review_query.update(review_update.model_dump(), synchronize_session=False)

        # Commit the changes to the database
        session.commit()

    except SQLAlchemyError as e:
        # Handle any database errors and rollback the session
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        # Close the session
        session.close()

    # Return the updated review
    return review_query.first()


def helper_delete_product(session, id:int):
    """
    Delete a product with the given id from the database.

    Args:
        session: SQLAlchemy session object.
        id (int): The id of the product to delete.
    
    Returns:
        Response: A response object with status code 204 if the product was successfully deleted.
    """

    try:
        # Query the database for the product with the given id
        product_query = session.query(Review).filter(Review.id == id)
        product = product_query.first()

        if product is None:
            # If the product does not exist, raise an HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} does not exist"
            )
        
        # Delete the product from the database
        product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors and rollback the transaction
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        # Close the session
        session.close()
    
    # Return a response with status code 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def helper_get_all_review_of_one_product(session, id:int):
    """
    Retrieve all the reviews of a given product ID from the database.

    Args:
        session: The session object for database operations.
        id (int): The ID of the product to retrieve reviews for.

    Raises:
        HTTPException: If there are no reviews for the given product ID.

    Returns:
        List[Review]: A list of Review objects representing the reviews of the product.
    """
    
    # Query the database for reviews of the given product ID
    review_query = session.query(Review).filter(Review.product_id == id)
    
    # Get all the reviews
    reviews = review_query.all()
    
    # If there are no reviews, raise an HTTPException with a 404 status code
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} does not have any review"
        )
        
    return reviews
