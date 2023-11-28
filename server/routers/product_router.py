from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas
from sqlalchemy import select
from sqlalchemy import func, select, outerjoin
from server.db import product_helper
router = APIRouter(prefix="/product", tags=["Product  CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: product_schemas.ProductCreate = Body(...)):
    """
    Create a new product along with associated images.
    
    Parameters:
    - product_data: Pydantic model containing product details.
    
    Returns:
    - Created Product.
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

    finally:
        session.close()

    return new_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
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


# Update a product 
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product(id: int, product_update: product_schemas.ProductUpadte = Body(...)):
    """
    Update a product by ID.

    Parameters:
    - id: ID of the product to be updated.
    - product_update: Pydantic model containing updated data.

    Returns:
    - Updated Product.
    """
    updated_product = product_helper.helper_update_product(session=session, id=id, product_update=product_update)
    return updated_product


@router.get("/{id}")
async def get_one_product(id: int):
    """
    Get a single product with its images based on the provided product ID.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Get the product with the given id but image it gets one image at a time and this issue needs to be fixed
    data = product_helper.helper_for_get_one_product(session= session, id=id)
    return data
    

@router.get("getproducts/{number}")
async def get_product_up_to_given_number(number: int):
    """
    Get a list of products with their images based on the provided number of rows you want.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - List of products with images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )

    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    return data

@router.get("getbyname/{product_name}/{number}")
async def get_product_by_name(product_name: str, number: int):
    """
    Get a multiple product with its images based on the provided product name.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )
    # Create a query to select the Product and ProductImage based on the provided product name
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.product_name == product_name)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    return data


@router.get("getbycategory/{category_id}/{number}")
async def get_product_by_name(category_id: int, number: int):
    """
    Get a multiple product with its images based on the provided product category.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )
    # Create a query to select the Product and ProductImage based on the provided product name
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.category_id == category_id)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    return data


@router.get("getbycategory_keyword/{category_id}/{search_keyword}/{number}")
async def get_product_by_name(category_id: int, search_keyword: str, number: int):
    """
    Get a multiple product with its images based on the provided product category.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )
    # Create a query to select the Product and ProductImage based on the provided product name
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.category_id == category_id)
        .filter(Product.product_name.contains(search_keyword))
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    return data