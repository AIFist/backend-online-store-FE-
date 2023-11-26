from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Review
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import reviews_schemas
from sqlalchemy import select
router = APIRouter(prefix="/review", tags=["Review  CRUD"])

@router.post("/", status_code=status.HTTP_201_CREATED)

async def create_review(product_data:  reviews_schemas.CreateReview= Body(...)):
    
    """
    Create a new review.

    Parameters:
    - product_data: Pydantic model containing review details.

    Returns:
    - Created Review.
    """
    
    try:
        db_review = Review(**product_data.model_dump())
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
    
    except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()  # Rollback the transaction

    finally:
            session.close()
    return db_review


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def review_update(id:int, review_update: reviews_schemas.UpdateReview=Body(...)):
    
    """
    Update a review by ID.

    Parameters:
    - id: ID of the review to be updated.
    - review_update: Pydantic model containing updated review data.

    Returns:
    - Updated Review.
    """
    try:
        review_query = session.query(Review).filter(Review.id == id)
        db_product = review_query.first()
        if db_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")
        
        
        review_query.update(review_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()  # Rollback the transaction

    finally:
            session.close()
    
    return review_query.first()