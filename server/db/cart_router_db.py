from fastapi import status,HTTPException
from server.models.models import Cart
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import cart_schemas

def create_product_cart(session, product_cart: cart_schemas.ProductCartCreate):
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

def update_product_cart(session, id: int, product_cart_update: cart_schemas.ProductCartUpdate):
    """
    Update a product cart by ID.

    Args:
    - id: ID of the product cart to be updated.
    - product_cart_update: ProductCartUpdate model containing updated data for the product cart.

    Returns:
    - The updated product cart.
    """
    try:
        # Query the product cart with the given id
        product_cart_query = session.query(Cart).filter(Cart.id == id)
        product_cart = product_cart_query.first()

        # If product cart does not exist, raise 404 error
        if product_cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product cart with id {id} does not exist")

        # Update the product cart with the data from the product_cart_update model
        product_cart_query.update(product_cart_update.model_dump(), synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()
    finally:
        # Close the session
        session.close()
        
    return product_cart_query.first()