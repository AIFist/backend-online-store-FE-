from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import cart_schemas
from server.db import cart_helper
from typing import List
from server.models.models import Cart
from server.utils import oauth2
router = APIRouter(prefix="/cart", tags=["Product Cart CRUD"])

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=cart_schemas.ProductCartCreateResponse,
)
async def create_product_cart(
    sub_product_cart: cart_schemas.SubProductCartCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new product cart.

    Args:
        sub_product_cart (cart_schemas.SubProductCartCreate): The sub product cart data.
        current_user (int): The user ID of the current user.

    Returns:
        cart_schemas.ProductCartCreateResponse: The created product cart data.
    """
    # Prepare the data for creating the product cart
    product_cart_data = {
        "user_id": current_user.id,
        "product_id": sub_product_cart.product_id,
        "quantity": sub_product_cart.quantity,
    }

    try:
        # Validate the data for creating the product cart
        validated_product_cart_data = cart_schemas.ProductCartCreate.model_validate(
            product_cart_data
        )
    except ValueError as e:
        print(f"An error occurred: {e}")

    # Create the product cart in the database
    created_product_cart = cart_helper.create_product_cart(
        session=session, product_cart=validated_product_cart_data
    )

    return created_product_cart
   

@router.put("/{id}", 
            status_code=status.HTTP_201_CREATED,
            response_model=cart_schemas.ProductCartUpdateResponse
            )
async def product_cart_update(
    id: int,
    product_cart_update: cart_schemas.ProductCartUpdate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
    ):
    """
    Update a product cart by ID.

    Args:
    - id: ID of the product cart to be updated.
    - product_cart_update: ProductCartUpdate model containing updated data for the product cart.

    Returns:
    - The updated product cart.
    """
    # Query the product cart by ID
    product_cart_query = session.query(Cart).filter(Cart.id == id)
    product_cart= product_cart_query.first()

    # Check if the current user is authorized to update the product cart
    if current_user.id != product_cart.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    
    # Update the product cart
    data = cart_helper.update_product_cart(
        session=session, id=id, product_cart_update=product_cart_update
    )
    
    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_cart(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a product cart by ID.

    Args:
    - id: ID of the product cart to be deleted.
    - current_user: The ID of the current user.

    Returns:
    - The deleted product cart.

    Raises:
    - HTTPException: If the current user is not authorized to perform the requested action.
    """
    # Retrieve the product cart from the database
    product_cart = session.query(Cart).filter(Cart.id == id).first()

    # Check if the current user is authorized to delete the product cart
    if current_user.id != product_cart.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    # Delete the product cart from the database
    data = cart_helper.delete_product_cart(session=session, id=id)

    return data



 # this endpoint should all product with prodect data
@router.get(
    "/allproducts",
    status_code=status.HTTP_200_OK,
    response_model=List[cart_schemas.ProductCartGetResponse]
)
async def get_all_product_cart(
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Get all products in the cart for a given user.

    Args:
        current_user (int): The ID of the user.

    Returns:
        List[cart_schemas.ProductCartGetResponse]: The cart data for the user.
    """
    # Get the ID of the current user
    user_id = int(current_user.id)
    
    # Retrieve all products in the cart for the given user
    data = cart_helper.get_all_product_for_cart(session=session, UserId=user_id)
    
    return data
