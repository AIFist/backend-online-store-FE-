from fastapi import status,HTTPException
from server.schemas import banners_schemas
from sqlalchemy.exc import SQLAlchemyError
from server.models.models import Banner

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
