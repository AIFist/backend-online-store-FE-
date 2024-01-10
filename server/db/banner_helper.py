from fastapi import status,HTTPException, Response
from server.schemas import banners_schemas
from sqlalchemy.exc import SQLAlchemyError
from server.models.models import Banner, Product

def helper_create_banner(session, banner: banners_schemas.CreateBanner):
    """
    Create a new banner in the database.

    Args:
        session: The SQLAlchemy session object.
        banner: An instance of CreateBanner schema representing the new banner.

    Returns:
        The newly created banner.

    Raises:
        HTTPException: If there is a foreign key constraint violation or other unprocessable entity error.
    """

    try:
        new_banner = Banner(**banner.model_dump())

        session.add(new_banner)
        session.commit()
        session.refresh(new_banner)
        return new_banner
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


def helper_delete_banner(session, banner_id: int):
    """
    Delete a banner from the database.

    Args:
        session: The SQLAlchemy session object.
        banner_id: The ID of the banner to delete.

    Returns:
        The deleted banner.

    Raises:
        HTTPException: If the banner with the given ID does not exist.
    """
    
    banner = session.query(Banner).filter(Banner.id == banner_id).first()
    if banner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found",
        )
    try:
        session.delete(banner)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


def helper_get_all_banners(session, number: int):
    """
    Get all banners from the database.

    Args:
        session: The SQLAlchemy session object.
        number: The number of banners to return.

    Returns:
        A list of banners.
    """
    # Query to get a list of product_id from the banners table
    banner_products = session.query(Banner.product_id).all()

    # Extract the product_ids from the result
    product_ids_list = [product_id for product_id, in banner_products]

    return product_ids_list