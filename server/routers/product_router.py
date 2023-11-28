from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
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
    
    data = product_helper.helper_create_product(session=session, product_data=product_data)
    return data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
    """
    res = product_helper.helper_for_deleting_product(session=session, id=id)
    return res


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
    Get a list of products with their images up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.

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
    Get multiple products with their images based on the provided product name.

    Args:
    - product_name (str): The name of the product.
    - number (int): The number of products to retrieve.

    Returns:
        dict: A dictionary containing the products and their images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )
    
    # Create a query to select the Product and ProductImage based on the provided product name
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.product_name == product_name)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )
    
    # Get the data using the helper function
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    
    return data


@router.get("getbycategory/{category_id}/{number}")
async def get_product_by_name(category_id: int, number: int):
    """
    Get multiple products with their images based on the provided category ID.

    Parameters:
    - category_id: The ID of the category.
    - number: The number of products to retrieve.

    Returns:
    - A list of products with their images.
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
    Get a multiple product with its images based on the provided product category and search keyword.

    Parameters:
    - category_id: The ID of the product category.
    - search_keyword: The search keyword to filter the products.
    - number: The maximum number of products to return.

    Returns:
    - A list of products with their images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )

    # Create a query to select the Product and ProductImage based on the provided category ID and search keyword
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.category_id == category_id)
        .filter(Product.product_name.contains(search_keyword))
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Call the helper function to execute the query and return the result
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=number)
    return data


@router.get("searchbyproductsize/{product_size}/{number}")
def get_product_by_size(product_size: str, number: int):
    """
    Get multiple products with their images based on the provided product size.

    Parameters:
    - product_size: The size of the product.
    - number: The maximum number of products to fetch.

    Returns:
    - A list of products with their images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])  # Count the number of rows
        .select_from(outerjoin(Product, ProductImage))  # Outer join Product and ProductImage tables
        .scalar_subquery()  # Get the count as a subquery
    )

    # Create a query to select the Product and ProductImage based on the provided product size
    query = (
        select(Product, ProductImage)  # Select both Product and ProductImage
        .outerjoin(ProductImage)  # Outer join Product and ProductImage tables
        .filter(Product.product_size.contains(product_size))  # Filter by product size has give product size keyword
        .limit(number)  # Limit the number of results
        .order_by(Product.id)  # Order by Product ID
        .distinct(Product.id)  # Remove duplicate Products
    )

    # Call the helper function to execute the query and return the result
    data = product_helper.helper_for_get_request(session=session, query=query, count_subquery=count_subquery, number=10)
    return data
