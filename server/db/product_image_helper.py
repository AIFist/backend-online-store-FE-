from server.models.models import ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_image_schemas
def helper_create_product_image(session, product_image:product_image_schemas.ProductImageCreate ):
    try:
        # Create a new ProductCategory instance using the data from the product_category model
        new_product_image = ProductImage(**product_image.model_dump())

        # Add the new_product_category to the session
        session.add(new_product_image)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_category with the latest data from the database
        session.refresh(new_product_image)
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()

    finally:
        # Close the session
        session.close()
    
    # Return the newly created ProductCategory
    return new_product_image