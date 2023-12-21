from fastapi import Body, status, Depends,HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import user_purchases_schemas
from server.db import  user_purchases_helper
from typing import List
from server.utils import oauth2
router = APIRouter(prefix="/user_purchases", tags=["User Purchases CRUD"])


@router.post("/create",
             status_code=status.HTTP_201_CREATED,
             response_model=user_purchases_schemas.SubUserPurchasesCreate
             )
async def create_user_purchase(
    sub_user_purchase: user_purchases_schemas.SubUserPurchasesCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new user purchase.

    Args:
        user_purchase (user_purchases_schemas.UserPurchasesCreate): The user purchase data.

    Returns:
        The created user purchase data.
    """
    user_purchase = {
        "user_id": current_user.id,
        "product_id": sub_user_purchase.product_id,
        "status": sub_user_purchase.status
    }
    try:
        # Validate the data for creating the user purchase
        user_purchase = user_purchases_schemas.UserPurchasesCreate.model_validate(user_purchase)
        
    except ValueError as e:
        print(f"An error occurred: {e}")
    # Create the user purchase in the database
    data = user_purchases_helper.helper_create_user_purchase(
        session=session, user_purchase=user_purchase
    )
    return data


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            response_model=user_purchases_schemas.UserPurchasesUpdateResponse
            )
async def user_purchase_update(
    id: int,
    user_purchase_update: user_purchases_schemas.UserPurchasesUpdate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Update a user purchase by ID.

    Args:
    - id: ID of the user purchase to be updated.
    - user_purchase_update: UserPurchasesUpdate model containing updated data for the user purchase.

    Returns:
    - The updated user purchase.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    data = user_purchases_helper.helper_update_user_purchase(
        session=session, id=id, user_purchase_update=user_purchase_update
    )
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_purchase(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Delete a user purchase by ID.

    Args:
    - id: ID of the user purchase to be deleted.

    Returns:
    - The deleted user purchase.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    data = user_purchases_helper.helper_delete_user_purchase(session=session, id=id)
    return data

@router.get("/", 
            status_code=status.HTTP_200_OK,
            response_model=List[user_purchases_schemas.UserPurchasesGetAll]
            )
async def get_all_user_purchase(current_user: int = Depends(oauth2.get_current_user)):
    """
    Get all user purchases.

    Returns:
    - A list of user purchases.
    """
    UserId = int(current_user.id)
    data = user_purchases_helper.helper_get_all_user_purchases(session=session,UserId=UserId)
    return data

@router.get("/{number}/{startindex}", status_code=status.HTTP_200_OK)
async def get_all_user_purchases_for_given_number(
    number: int,
    startindex: int,
    current_user: int = Depends(oauth2.get_current_user),
    
    # current_user: int = Depends(oauth2.get_current_user),
):
    """
    Get all user purchases for a given status.

    Returns:
    - A list of user purchases for the given status.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
   # this function does not retrun given numbers of user purchases 
    data= user_purchases_helper.helper_get_all_user_purchases_for_given_number(session=session, startindex=startindex,number=number)
    return data
