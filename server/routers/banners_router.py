from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import banners_schemas
from server.db import banner_helper
from typing import List
from server.utils import oauth2
from server.db.fliter_product_with_reviews_helper import get_product_details_query
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/banner", tags=["Banner CRUD"])

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=banners_schemas.BannerCreateResponse,
)
async def create_banner(
    banner: banners_schemas.CreateBanner = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new banner.

    Args:
        banner (BannerCreate): Data for the new banner.
        current_user (int): ID of the current user.

    Returns:
        BannerCreateResponse: Newly created Banner.
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    # Create the banner using the helper function
    data = banner_helper.helper_create_banner(session=session, banner=banner)
    return data


@router.delete("/delete/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(
    banner_id: int,
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Deletes a banner by ID.

    Parameters:
        - `banner_id` (int): The ID of the banner to be deleted.
        - `current_user` (int, optional): The ID of the current user. Defaults to `Depends(oauth2.get_current_user)`.

    Raises:
        - `HTTPException`: If the current user does not have admin role.

    Returns:
        - `None`
    """
    # Check if the current user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    # Delete the banner by ID
    data = banner_helper.helper_delete_banner(session=session, banner_id=banner_id)

    # Return the deleted banner
    return data


@router.get("/getall/{number}", 
            status_code= status.HTTP_200_OK,
            response_model=List[banners_schemas.BannerGetAllResponse])
def get_all_banners(
    number: int, 
    ):
    """
    Retrieve all banners and their details.

    Parameters:
        number (int): The number of banners to retrieve.

    Returns:
        List[banners_schemas.BannerGetAllResponse]: A list of banner objects containing their details.

    Raises:
        HTTPException: If an error occurs during the retrieval process.

    Example Usage:
         get_all_banners(10)
        [
            {
                "id": 1,
                "name": "Banner 1",
                "image_url": "https://example.com/banner1.jpg"
            },
            {
                "id": 2,
                "name": "Banner 2",
                "image_url": "https://example.com/banner2.jpg"
            },
            ...
        ]
    """
    
    # Get all banners
    product_ids = banner_helper.helper_get_all_banners(session=session, number=number)
    # Generate the query to get the details of the products
    query = get_product_details_query(product_ids)

    try:
        # Execute the query and retrieve the results
        result = session.execute(query).all()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Reverse the order of the results
    re = result[::-1]

    return re
