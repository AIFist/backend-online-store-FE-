from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models import ProductCategory
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_cat_schemas


def helper_create_product_category(session, product_category: product_cat_schemas.ProductCategoryCreate ):
    try:
        # Create a new ProductCategory instance using the data from the product_category model
        new_product_category = ProductCategory(**product_category.model_dump())

        # Add the new_product_category to the session
        session.add(new_product_category)

        # Commit the changes to the database
        session.commit()

        # Refresh the new_product_category with the latest data from the database
        session.refresh(new_product_category)
    
    except SQLAlchemyError as e:
        # Print the error message
        print(f"An error occurred: {e}")

        # Rollback the transaction
        session.rollback()

    finally:
        # Close the session
        session.close()
    
    # Return the newly created ProductCategory
    return new_product_category

def helper_delete_product_category(session, id: int):
    # Query the product category by ID
    product_cat_query = session.query(ProductCategory).filter(ProductCategory.id == id)
    product_cat = product_cat_query.first()
    
    # Check if the product category exists
    if product_cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} does not exist")

    # Delete the product category
    product_cat_query.delete(synchronize_session=False)
    session.commit()

    # Return a response with no content
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def helper_update_product_category(session, id: int, productcat_update: product_cat_schemas.ProductCategoryUpdate):
    try: 
        # Retrieve the product category from the database
        product_category = session.query(ProductCategory).filter(ProductCategory.id == id).first()
        
        # Check if the product category exists
        if not product_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product Category with id {id} does not exist")
        
        # Update the parent category ID if it is not provided
        if productcat_update.parent_category_id is None:
            productcat_update.parent_category_id = product_category.parent_category_id
        
        # Update the product category in the database
        session.query(ProductCategory).filter(ProductCategory.id == id).update(productcat_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
    
    # Retrieve and return the updated product category
    return session.query(ProductCategory).filter(ProductCategory.id == id).first()


def helper_get_product_category(session):
     # Query all product categories
    categories = session.query(ProductCategory.id, ProductCategory.category_name).all()
    
    # Create a list of tuples with category id and name
    result = [(category.id, category.category_name) for category in categories]
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category table is empty")
        

def helper_get_one_product_category(session, id: int):
    product_category = session.query(ProductCategory).filter(ProductCategory.id == id).first()
    if not product_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} was not found")
        
    return product_category