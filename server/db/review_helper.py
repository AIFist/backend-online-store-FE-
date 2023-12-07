from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models import Review
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import reviews_schemas

def helper_create_review(session, product_data: reviews_schemas.CreateReview ):
    try:
        db_review = Review(**product_data.model_dump())
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing your request. \n most probably product with id {db_review.product_id} does not exist or user with id {db_review.user_id} does not exist.")

    finally:
        session.close()

    return db_review


def helper_review_update(session, id:int , review_update: reviews_schemas.UpdateReview ):
    try:
        review_query = session.query(Review).filter(Review.id == id)
        review= review_query.first()
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with id {id} does not exist")

        review_query.update(review_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        session.close()

    return review_query.first()

def helper_delete_product(session, id:int):
    try:
        product_query = session.query(Review).filter(Review.id == id)
        product = product_query.first()
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product Category with id {id} does not exist")
        
        product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()  # Rollback the transaction

    finally:
            session.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def helper_get_all_review_of_one_product(session, id:int):
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