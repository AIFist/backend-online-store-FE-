from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import banners_schemas
from server.db import banner_helper
from typing import List
from server.utils import oauth2

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