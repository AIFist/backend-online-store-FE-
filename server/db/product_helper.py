from fastapi import HTTPException, status,Response
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas
from typing import List


# TODO remove following commented function when you resolve the issue in helper_for_get_one_product

# def helper_for_get_request(session, query, count_subquery, number):
#     # Check if the number of rows in the table is less than the specified number
#     if session.execute(select([func.count()]).select_from(query.alias())).scalar() < number:
#         query = query.limit(count_subquery)  # Limit the main query by the count
        
#     # Execute the query and get the results
#     result = session.execute(query).all()
#     # Execute the query and get the first result
#     # If no result is found, raise an HTTPException with a 404 status code
#     if result is None:
#         raise HTTPException(status_code=404, detail=f"Product not found")
#     # Extract the Product and ProductImage from the result
#     products_with_images = []
#     for product, image in result:
#         product_with_images = {
#             "id": product.id,
#             "product_name": product.product_name,
#             "description": product.description,
#             "price": product.price,
#             "stock_quantity": product.stock_quantity,
#             "product_size": product.product_size,
#             "SKU": product.SKU,
#             "target_audience": product.target_audience,
#             "product_color": product.product_color,
#             "created_at": product.created_at,
#             "category_id": product.category_id,
#             "images": [{"id": image.id, "image_path": image.image_path} for image in product.images],
#         }
#         products_with_images.append(product_with_images)

#     return products_with_images



def helper_for_get_one_product(session, id: int):
    """
    Retrieve a single product with its images from the database based on the provided ID.
    Args:
        session (Session): The SQLAlchemy session.
        id (int): The ID of the product to retrieve.
    Returns:
        dict: A dictionary containing the product information and its images.
    """
    # Create a query to select the Product and ProductImage based on the provided ID
    query = (
        select(Product, ProductImage)
        .join(ProductImage)
        .filter(Product.id == id)
        .order_by(Product.id)
    )
    # Execute the query and get all results
    results = session.execute(query).all()
    
    # If no result is found, raise an HTTPException with a 404 status code
    if not results:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

    # Extract the Product and ProductImage from the result
    product, images = results[0]

    # Create a dictionary to store the product information
    product_with_images = {
        "id": product.id,
        "product_name": product.product_name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "product_size": product.product_size,
        "SKU": product.SKU,
        "target_audience": product.target_audience,
        "product_color": product.product_color,
        "created_at": product.created_at,
        "category_id": product.category_id,
        "images": [{"id": image.id, "image_path": image.image_path} for image in product.images],
    }

    # Return the product_with_images dictionary
    return product_with_images



def helper_update_product(session, id:int, product_update:product_schemas.ProductUpadte):
    """
    Updates a product in the database with the provided ID and new data.
    Args:
        session: The database session
        id (int): The ID of the product to be updated
        product_update (product_schemas.ProductUpadte): The new data for the product
    Returns:
        The updated product
    """
    try:
        # Retrieve the product from the database based on the provided ID
        product_query = session.query(Product).filter(Product.id == id)
        db_product = product_query.first()
        if db_product is None:
            # If the product does not exist, raise an HTTP 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")

        # Update the product with the new data
        product_query.update(product_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        # If an error occurs during the update, print the error and rollback the transaction
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        # Close the database session
        session.close()

    # Return the updated product
    return product_query.first()



def helper_for_deleting_product(session, id:int):
    """
    Deletes a product from the database with the given ID.
    Args:
        session (Session): The SQLAlchemy session object.
        id (int): The ID of the product to delete.
    Returns:
        Response: A response object with status code 204 if successful.
    """
    try:
        # Query the product with the given id
        product_query = session.query(Product).filter(Product.id == id)
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


def helper_create_product(session, product_data: product_schemas.ProductCreate):
    """
    Creates a new product in the database.
    Args:
        session: SQLAlchemy session object.
        product_data: ProductCreate object containing the data for the new product.
    Returns:
        The newly created product.
    Raises:
        HTTPException: If there is a foreign key constraint violation or other unprocessable entity error.
    """
    try:
        # Convert the Pydantic model to a SQLAlchemy model
        new_product = Product(**product_data.model_dump(exclude={"images"}))

        # Create product images and associate with the product
        for image_data in product_data.images:
            image = ProductImage(**image_data.model_dump())
            new_product.images.append(image)

        # Add the product to the session and commit
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Foreign key constraint violation or other unprocessable entity error",
        )

    finally:
        session.close()

    return new_product
# work on this function to get data from user in bulk for product and save it in the database
def helper_create_products_bulk(session, products_data: List[product_schemas.ProductCreate]):
    pass