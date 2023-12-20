from fastapi import Body, status, Depends, HTTPException
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import cart_schemas
from server.db import cart_helper
from typing import List
from server.models.models import Cart
from server.utils import oauth2
router = APIRouter(prefix="/cart", tags=["Product Cart CRUD"])

@router.post("/create", 
             status_code=status.HTTP_201_CREATED,
             response_model=cart_schemas.ProductCartCreateResponse
             )
async def create_product_cart(
    sub_product_cart: cart_schemas.SubProductCartCreate = Body(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new product cart.

    Args:
        product_cart (cart_schemas.ProductCartCreate): The product cart data.

    Returns:
        The created product cart data.
    """
    product_cart = {
        "user_id": current_user.id,
        "product_id": sub_product_cart.product_id,
        "quantity": sub_product_cart.quantity
    }
    try:
        # Validate the data for creating the product cart
        product_cart = cart_schemas.ProductCartCreate.model_validate(product_cart)
    except ValueError as e:
        print(f"An error occurred: {e}")
    

    # Create the product cart in the database
    data = cart_helper.create_product_cart(
        session=session, product_cart=product_cart
    )
    
    return data
   

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
    product_cart_query = session.query(Cart).filter(Cart.id == id)
    product_cart= product_cart_query.first()

    # Check if the current user is authorized to update the review
    if current_user.id != product_cart.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
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

    Returns:
    - The deleted product cart.
    """
    product_cart_query = session.query(Cart).filter(Cart.id == id)
    product_cart = product_cart_query.first()

    # Check if the current user is authorized to update the review
    if current_user.id != product_cart.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    data = cart_helper.delete_product_cart(session=session, id=id)
    return data



 # this endpoint should all product with prodect data
@router.get("/allproduct/{UserId}",
            status_code=status.HTTP_200_OK,
            response_model=List[cart_schemas.ProductCartGetResponse]
            )
async def get_all_product_cart(UserId: int):
    """
    Get all products in the cart for a given user.

    Args:
        UserId (int): The ID of the user.

    Returns:
        data: The cart data for the user.
    """
    # Retrieve all products in the cart for the given user
    data = cart_helper.get_all_product_for_cart(session=session, UserId=UserId)
    
    return data
