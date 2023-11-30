from fastapi import status,HTTPException, Response
from server.schemas import favorites_schemas
from server.models.models import Favorite as Favorites
from server.models.models import UserPurchase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from server.schemas import user_purchases_schemas

def helper_create_user_purchase(session,user_purchase: user_purchases_schemas.UserPurchasesCreate):
    """
    Create a new user purchase.

    Args:
    - user_purchase: UserPurchasesCreate model containing data for the new user purchase.

    Returns:
    - The newly created user purchase.
    """

    try:
        # Create a new UserPurchase instance using the data from the user_purchase model
        new_user_purchase = UserPurchase(**user_purchase.model_dump())

        # Add the new_user_purchase to the session
        session.add(new_user_purchase)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_user_purchase with the latest data from the database
        session.refresh(new_user_purchase)

    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transactionraise
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing your request. \n most probably product with id {new_user_purchase.product_id} does not exist or user with id {new_user_purchase.user_id} does not exist.")
    finally:
        # Close the session
        session.close()
    
        session.rollback()
        
    return new_user_purchase