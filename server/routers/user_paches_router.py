from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import user_purchases_schemas
from server.db import  user_purchases_helper

router = APIRouter(prefix="/user_purchases", tags=["User Purchases CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_purchase(
    user_purchase: user_purchases_schemas.UserPurchasesCreate = Body(...)
):
    """
    Creates a new user purchase.

    Args:
        user_purchase (user_purchases_schemas.UserPurchasesCreate): The user purchase data.

    Returns:
        The created user purchase data.
    """

    # Create the user purchase in the database
    data = user_purchases_helper.helper_create_user_purchase(
        session=session, user_purchase=user_purchase
    )
    return data