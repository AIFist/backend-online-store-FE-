from fastapi import status,HTTPException, Response
from server.models.models import Cart, Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import cart_schemas
from sqlalchemy.orm import joinedload
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )
    finally:
        # Close the session
        session.close()
        
    return product_cart_query.first()


def delete_product_cart(session, id:int):
    try:
        # Query the product with the given id
        product_query = session.query(Cart).filter(Cart.id == id)
        product = product_query.first()

        # If product does not exist, raise 404 error
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")

        # Delete the product
        product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_all_product_cart(session, UserId: int):
    try:
        # Query the carts with the given user_id
        carts = session.query(Cart).filter(Cart.user_id == UserId).all()

        # If no carts are found, you might want to handle it accordingly
        if not carts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No products found for user with id {UserId}")

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return carts

def get_all_product_for_cart(session, UserId:int):
    try:
        # Query the carts, join with the Product and ProductImage tables
        carts = (
            session.query(Cart)
            .join(Product, Cart.product_id == Product.id)
            .outerjoin(ProductImage, ProductImage.product_id == Product.id)
            .filter(Cart.user_id == UserId)
            .options(
                joinedload(Cart.product)  # Use joinedload to eagerly load the associated Product
                .joinedload(Product.images)  # Use joinedload to eagerly load the associated ProductImage
            )
            .all()
        )

        # If no carts are found, you might want to handle it accordingly
        if not carts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No products found for user with id {UserId}")

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return carts
