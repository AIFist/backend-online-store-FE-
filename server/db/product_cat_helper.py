from fastapi import status,HTTPException, Response
from server.models.models import ProductCategory
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_cat_schemas
from sqlalchemy.orm import aliased

def helper_create_product_category(session, product_category: product_cat_schemas.ProductCategoryCreate ):
    """
    Create a new product category and save it to the database.

    Args:
        session: The SQLAlchemy session object.
        product_category: An instance of the ProductCategoryCreate model.

    Returns:
        The newly created ProductCategory instance.
    """
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
    """
    Deletes a product category by ID.

    Args:
        session: The database session.
        id: The ID of the product category to delete.

    Raises:
        HTTPException: If the product category does not exist.

    Returns:
        Response: A response with no content.
    """
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
    """
    Update a product category in the database.

    Args:
        session (sqlalchemy.orm.session.Session): SQLAlchemy session object.
        id (int): ID of the product category to update.
        productcat_update (product_cat_schemas.ProductCategoryUpdate): Object containing the updated data.

    Returns:
        product_cat_schemas.ProductCategory: The updated product category.

    Raises:
        HTTPException: If the product category does not exist.
    """

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
        session.query(ProductCategory).filter(ProductCategory.id == id).update(productcat_update.model_dump(),
                                                                              synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

    # Retrieve and return the updated product category
    return session.query(ProductCategory).filter(ProductCategory.id == id).first()


def helper_get_product_category(session):
    """
    Retrieves all product categories from the database.

    Args:
        session: The SQLAlchemy database session.

    Returns:
        A list of dictionaries with category id and name.

    Raises:
        HTTPException: If the product category table is empty.
        HTTPException: If there is a database error while retrieving product categories.
    """
    try:
        # Query all product categories
        categories = session.query(ProductCategory.id, ProductCategory.category_name).all()

        # Create a list of dictionaries with category id and name
        result = [{"id": int(category.id), "category_name": category.category_name} for category in categories]
        if result:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category table is empty")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error while retrieving product categories")

def helper_get_one_product_category(session, id: int):
    """
    Retrieve a single product category from the database by ID.
    
    Args:
        session: The database session object.
        id: The ID of the product category to retrieve.
    
    Returns:
        The product category object.
    
    Raises:
        HTTPException: If the product category with the given ID is not found.
    """
    try:
        # Query the database for the product category with the specified ID
        product_category = session.query(ProductCategory).filter(ProductCategory.id == id).first()
        
        # If the product category does not exist, raise an HTTPException
        if not product_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product Category with id {id} was not found")
            
        return product_category
    except SQLAlchemyError as e:
        # If there is an error during the database operation, rollback the session,
        # raise an HTTPException with a 500 status code, and provide an error message
        print(f"An error occurred: {e}")
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error while retrieving product category")


def helper_get_all_subcategories(session):
    """
    Retrieves all subcategories for a given category.

    :param session: The database session.
    :type session: sqlalchemy.orm.session.Session
    :return: A list of dictionaries representing the categories and their subcategories.
    :rtype: list
    """
    # Alias for the self-referencing relationship
    sub_category_alias = aliased(ProductCategory)

    # Query to retrieve products and their subcategories
    result = (
        session.query(
            ProductCategory.id.label('id'),
            ProductCategory.category_name.label('category_name'),
            sub_category_alias.id.label('sub_id'),
            sub_category_alias.category_name.label('sub_category_name')
        )
        .outerjoin(sub_category_alias, ProductCategory.subcategories)
        .filter(ProductCategory.parent_category_id.is_(None))  # Assuming root categories have parent_category_id as NULL
        .all()
    )

    # Organizing the result into the desired structure
    output = []
    current_category = None

    for row in result:
        if not current_category or current_category['id'] != row.id:
            current_category = {
                'id': row.id,
                'category_name': row.category_name,
                'sub_cate': []
            }
            output.append(current_category)

        if row.sub_id is not None:
            current_category['sub_cate'].append({
                'id': row.sub_id,
                'category_name': row.sub_category_name
            })

    return output