from fastapi import status,HTTPException, Response
from server.schemas import favorites_schemas
from server.models.models import Favorite as Favorites
from server.models.models import Product, User , ProductImage
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload


def helper_create_product_favorite(session, product_favorite: favorites_schemas.ProductFavoriteCreate):
    """
    Create a new product favorite.

    Args:
    - session: SQLAlchemy session object
    - product_favorite: ProductFavoriteCreate model containing data for the new product favorite.

    Returns:
    - The newly created product favorite.
    """
    try:
        # Create a new ProductFavorite instance using the data from the product_favorite model
        new_product_favorite = Favorites(**product_favorite.model_dump())

        # Add the new_product_favorite to the session
        session.add(new_product_favorite)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_favorite with the latest data from the database
        session.refresh(new_product_favorite)

    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )
    finally:
        # Close the session
        session.close()
        
    # Return the newly created product favorite
    return new_product_favorite


def helper_delete_product_favorite(session, id: int):
    """
    Delete a product favorite by ID.

    Args:
    - session: SQLAlchemy session object
    - id: ID of the product favorite to be deleted.

    Returns:
    - The deleted product favorite.
    """
    try:
    # Declare Favorite variable before using it in the query

        # Query the product with the given id
        Favorite_product_query = session.query(Favorites).filter(Favorites.id == id)
        Favorite = Favorite_product_query.first()

        # If product does not exist, raise 404 error
        if Favorite is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")

        # Delete the product
        Favorite_product_query.delete(synchronize_session=False)
        session.commit()

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def helper_get_all_product_favorite(session, UserId):
    """
    Get all product favorites.

    Args:
    - session: SQLAlchemy session object

    Returns:
    - A list of product favorites.
    """
    try:
        fav = (
            session.query(Favorites)
            .join(Product, Favorites.product_id == Product.id)
            .outerjoin(ProductImage, ProductImage.product_id == Product.id)
            .filter(Favorites.user_id == UserId)
            .options(
                joinedload(Favorites.product)  # Use joinedload to eagerly load the associated Product
                .joinedload(Product.images)  # Use joinedload to eagerly load the associated ProductImage
            )
            .all()
        )
        data = session.query(Favorites).filter(Favorites.user_id == UserId).all()
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {UserId} does not exist")
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()
    return data
    
