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