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

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def user_purchase_update(id: int, user_purchase_update: user_purchases_schemas.UserPurchasesUpdate = Body(...)):
    """
    Update a user purchase by ID.

    Args:
    - id: ID of the user purchase to be updated.
    - user_purchase_update: UserPurchasesUpdate model containing updated data for the user purchase.

    Returns:
    - The updated user purchase.
    """
    data = user_purchases_helper.helper_update_user_purchase(
        session=session, id=id, user_purchase_update=user_purchase_update
    )
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_purchase(id: int):
    """
    Delete a user purchase by ID.

    Args:
    - id: ID of the user purchase to be deleted.

    Returns:
    - The deleted user purchase.
    """
    data = user_purchases_helper.helper_delete_user_purchase(session=session, id=id)
    return data