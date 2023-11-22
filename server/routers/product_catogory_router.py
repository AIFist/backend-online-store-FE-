from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import ProductCategory
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_cat_schemas



router = APIRouter(prefix="/product_cat", tags=["Product category CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_category(product_category: product_cat_schemas.ProductCategoryCreate = Body(...)):
    """
    Create a new product category.

    Parameters:
    - product_category: ProductCategoryCreate model from product_cat_schemas containing data for the new category.
    - session: SQLAlchemy Session dependency.

    Returns:
    - Newly created ProductCategory.
    """
    db_product_category = ProductCategory(**product_category.model_dump())
    session.add(db_product_category)
    session.commit()
    session.refresh(db_product_category)
    return db_product_category


# Delete a product category
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_category(id: int,):
    """
    Delete a product category by ID.

    Parameters:
    - id: ID of the product category to be deleted.
    - session: SQLAlchemy Session dependency.

    Returns:
    - Response with 204 status code if successful.
    """
    product_cat_query = session.query(ProductCategory).filter(ProductCategory.id == id)
    product_cat = product_cat_query.first()
    if product_cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} does not exist")
    
    product_cat_query.delete(synchronize_session=False)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a product category
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product_category(id: int, prouctcat_update: product_cat_schemas.ProductCategoryUpdate = Body(...)):
    """
    Update a product category by ID.

    Parameters:
    - id: ID of the product category to be updated.
    - prouctcat_update: ProductCategoryUpdate model from product_cat_schemas containing updated data.
    - session: SQLAlchemy Session dependency.

    Returns:
    - Updated ProductCategory.
    """
    ProductCategory_query = session.query(ProductCategory).filter(ProductCategory.id == id)
    ProductCategory1 = ProductCategory_query.first()
    if ProductCategory1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    
    ProductCategory_query.update(prouctcat_update.model_dump(), synchronize_session=False)
    session.commit()
    return ProductCategory_query.first()


# Get all product categories with their IDs and names
@router.get("/all")
async def get_product_category():
    """
    Get all product categories with their IDs and names.

    Parameters:
    - session: SQLAlchemy Session dependency.

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
    ProductCategory1 = session.query(ProductCategory).filter(ProductCategory.id == id).first()
    if not ProductCategory1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product Category with id {id} was not found")
        
    return ProductCategory1