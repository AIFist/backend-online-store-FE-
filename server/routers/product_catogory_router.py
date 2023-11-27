from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import ProductCategory
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_cat_schemas



router = APIRouter(prefix="/product_cat", tags=["Product category CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_category(product_category: product_cat_schemas.ProductCategoryCreate = Body(...)) -> ProductCategory:
    """
    Create a new product category.

    Parameters:
    - product_category: ProductCategoryCreate model from product_cat_schemas containing data for the new category.

    Returns:
    - Newly created ProductCategory.
    """
    try:
        new_product_category = ProductCategory(**product_category.model_dump())
        session.add(new_product_category)
        session.commit()
        session.refresh(new_product_category)
    
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        session.close()
    
    return new_product_category


# Delete a product category
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_category(id: int):
    """
    Delete a product category by its ID.
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


# Update a product category
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product_category(id: int, productcat_update: product_cat_schemas.ProductCategoryUpdate = Body(...)):
    """
    Update a product category by ID.

    Parameters:
    - id: ID of the product category to be updated.
    - productcat_update: ProductCategoryUpdate model containing updated data.

    Returns:
    - Updated ProductCategory.
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
        session.query(ProductCategory).filter(ProductCategory.id == id).update(productcat_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
    
    # Retrieve and return the updated product category
    return session.query(ProductCategory).filter(ProductCategory.id == id).first()


# Get all product categories with their IDs and names
@router.get("/all")
async def get_product_category():
    """
    Get all product categories with their IDs and names.

    Returns:
    - List of tuples containing (category_id, category_name).
    """
    categories = session.query(ProductCategory.id, ProductCategory.category_name).all()
    result = [(category.id, category.category_name) for category in categories]
    return result

# Get a specific product category by ID
@router.get("/{id}")
async def get_one_product_category(id: int):
    """
    Get a specific product category by ID.

    Parameters:
    - id: ID of the product category to retrieve.
    - session: SQLAlchemy Session dependency.

    Returns:
    - ProductCategory with the specified ID.
    """
    product_category = session.query(ProductCategory).filter(ProductCategory.id == id).first()
    if not product_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} was not found")
        
    return product_category
