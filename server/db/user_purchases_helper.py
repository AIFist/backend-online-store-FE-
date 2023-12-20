from fastapi import status,HTTPException, Response
from server.models.models import UserPurchase, Product, ProductImage
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
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )
    finally:
        # Close the session
        session.close()
    
        session.rollback()
        
    return new_user_purchase

def helper_update_user_purchase(session, id: int, user_purchase_update: user_purchases_schemas.UserPurchasesUpdate):
    """
    Update a user purchase record in the database with the given ID.

    Args:
        session: The SQLAlchemy session object.
        id: The ID of the user purchase to update.
        user_purchase_update: An instance of the UserPurchasesUpdate model containing the updated data.

    Returns:
        The updated user purchase record.

    Raises:
        HTTPException: If the user purchase with the given ID does not exist.
    """
    try:
        # Query the user purchase with the given ID
        user_purchase_query = session.query(UserPurchase).filter(UserPurchase.id == id)
        user_purchase = user_purchase_query.first()

        # If user purchase does not exist, raise 404 error
        if user_purchase is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User purchase with id {id} does not exist")

        # Update the user purchase with the data from the user_purchase_update model
        user_purchase_query.update(user_purchase_update.model_dump(), synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
    finally:
        # Close the session
        session.close()

    return user_purchase_query.first()


def helper_delete_user_purchase(session, id: int):
    """
    Delete a user purchase record from the database with the given ID.

    Args:
        session: The SQLAlchemy session object.
        id: The ID of the user purchase to delete.

    Returns:
        The deleted user purchase record.

    Raises:
        HTTPException: If the user purchase with the given ID does not exist.
    """
    try:
        # Query the user purchase with the given ID
        user_purchase_query = session.query(UserPurchase).filter(UserPurchase.id == id)
        user_purchase = user_purchase_query.first()

        # If user purchase does not exist, raise 404 error
        if user_purchase is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User purchase with id {id} does not exist")

        # Delete the user purchase
        user_purchase_query.delete(synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
    finally:
        # Close the session
        session.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def helper_get_all_user_purchases(session, UserId:int):
    """
    Get all user purchases from the database.

    Args:
        session: The SQLAlchemy session object.

    Returns:
        A list of all user purchases.
    """
    try:
        # Query the carts, join with the Product and ProductImage tables
        userPurchase = (
            session.query(UserPurchase)
            .join(Product, UserPurchase.product_id == Product.id)
            .outerjoin(ProductImage, ProductImage.product_id == Product.id)
            .filter(UserPurchase.user_id == UserId)
            .options(
                joinedload(UserPurchase.product)  # Use joinedload to eagerly load the associated Product
                .joinedload(Product.images)  # Use joinedload to eagerly load the associated ProductImage
            )
            .all()
        )

        # If no carts are found, you might want to handle it accordingly
        if not userPurchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No products found for user with id {UserId}")

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return userPurchase


def helper_get_all_user_purchases_for_given_number(session, startindex: int, number: int):
    """
    Get user purchases from the database within a specified range.

    Args:
        session: The SQLAlchemy session object.
        startindex: The starting index for fetching user purchases.
        number: The number of user purchases to retrieve.

    Returns:
        A list of user purchases within the specified range.
    """
    pass