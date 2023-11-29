from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Cart
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import cart_schemas

router = APIRouter(prefix="/productcart", tags=["Product Cart CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_cart(product_cart: cart_schemas.ProductCartCreate = Body(...)):
    """
    Create a new product in the cart.

    Args:
    - product_cart: ProductCartCreate model containing data for the new product cart.

    Returns:
    - The newly created product cart.
    """
    try:
        # Create a new ProductCart instance using the data from the product_cart model
        new_product_cart = Cart(**product_cart.model_dump())

        # Add the new_product_cart to the session
        session.add(new_product_cart)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_cart with the latest data from the database
        session.refresh(new_product_cart)
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing your request. \n most probably product with id {product_cart.product_id} does not exist or user with id {product_cart.user_id} does not exist.")
    finally:
        # Close the session
        session.close()
    
    # Return the newly created product cart
    return new_product_cart
