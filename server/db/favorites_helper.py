from fastapi import status,HTTPException
from server.schemas import favorites_schemas
from server.models.models import Favorite
from sqlalchemy.exc import SQLAlchemyError
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
        new_product_favorite = Favorite(**product_favorite.model_dump())

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing your request. \n most probably product with id {product_favorite.product_id} does not exist or user with id {product_favorite.user_id} does not exist.")
    finally:
        # Close the session
        session.close()
        
    # Return the newly created product favorite
    return new_product_favorite