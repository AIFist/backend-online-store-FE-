from fastapi import Body, status
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.schemas import cart_schemas
from server.db import cart_router_db

router = APIRouter(prefix="/cart", tags=["Product Cart CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_cart(
    product_cart: cart_schemas.ProductCartCreate = Body(...)
):
    """
    Creates a new product cart.

    Args:
        product_cart (cart_schemas.ProductCartCreate): The product cart data.

    Returns:
        The created product cart data.
    """

    # Create the product cart in the database
    data = cart_router_db.create_product_cart(
        session=session, product_cart=product_cart
    )
    
    return data
   

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def product_cart_update(id: int, product_cart_update: cart_schemas.ProductCartUpdate = Body(...)):
    """
    Update a product cart by ID.

    Args:
    - id: ID of the product cart to be updated.
    - product_cart_update: ProductCartUpdate model containing updated data for the product cart.

    Returns:
    - The updated product cart.
    """
    data = cart_router_db.update_product_cart(
        session=session, id=id, product_cart_update=product_cart_update
    )
    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_cart(id: int):
    """
    Delete a product cart by ID.

    Args:
    - id: ID of the product cart to be deleted.

    Returns:
    - The deleted product cart.
    """
    data = cart_router_db.delete_product_cart(session=session, id=id)
    return data

@router.get("{UserId}", status_code=status.HTTP_200_OK)
async def get_all_product_cart(UserId: int):
    """
    Retrieve all product carts for a user.

    Args:
    - UserId: ID of the user for which to retrieve product carts.

    Returns:
    - A list of product carts for the specified user.
    """
    data = cart_router_db.get_all_product_cart(session=session, UserId=UserId)
    return data

@router.get("/allproduct/{UserId}")
async def get_all_product_cart(UserId: int):
    """
    Get all products in the cart for a given user.

    Args:
        UserId (int): The ID of the user.

    Returns:
        data: The cart data for the user.
    """
    # Retrieve all products in the cart for the given user
    data = cart_router_db.get_all_product_cart(session=session, UserId=UserId)
    
    return data
