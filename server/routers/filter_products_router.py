from fastapi.routing import APIRouter
from server.models.models1 import session
from server.db import filter_products_helper

router = APIRouter(prefix="/productfilter", tags=["Filters for Product Endpoints"])

@router.get("/getproducts/{number}/{startindex}")
async def get_product_up_to_given_number(number: int, startindex: int):
    """
    Get a list of products with their images up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.
    - startindex: The starting index of the rows to retrieve.

    Returns:
    - List of products with images.
    """

    query = filter_products_helper.get_products(session=session, number=number, startindex=startindex)
    
    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data



@router.get("/getbyname/{product_name}/{number}/{startindex}")
async def get_product_by_name(product_name: str, number: int, startindex: int):
    """
    Get multiple products with their images based on the provided product name.

    Args:
    - product_name (str): The name of the product.
    - number (int): The number of products to retrieve.
    - startindex (int): The starting index for retrieving the products.

    Returns:
        dict: A dictionary containing the products and their images.
    """
    query = filter_products_helper.get_product_by_name(session=session, product_name=product_name, number=number, startindex=startindex)

    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data


@router.get("/getbycategory/{category_id}/{number}/{startindex}")
async def get_product_by_name(category_id: int, number: int, startindex: int):
    """
    Get multiple products with their images based on the provided category ID.

    Parameters:
    - category_id: The ID of the category.
    - number: The number of products to retrieve.
    - startindex: The starting index of the products to retrieve.

    Returns:
    - A list of products with their images.
    """
    # Create the main query
    query = filter_products_helper.get_product_by_category(session=session, category_id=category_id, number=number, startindex=startindex)
    # Get the data using the helper function
    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data


@router.get("/getbycategory_keyword/{category_id}/{search_keyword}/{number}/{startindex}")
async def get_product_by_name(category_id: int, search_keyword: str, number: int, startindex: int):
    """
    Get a list of products with their images based on the provided product category and search keyword.

    Parameters:
    - category_id: The ID of the product category.
    - search_keyword: The search keyword to filter the products.
    - number: The maximum number of products to return.
    - startindex: The starting index for pagination.

    Returns:
    - A list of products with their images.
    """
    # Create the main query
    query = filter_products_helper.get_product_by_category_keyword(session=session, category_id=category_id, search_keyword=search_keyword, number=number, startindex=startindex)

    # Get the data using the helper function
    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data


@router.get("/searchbyproductsize/{product_size}/{number}/{startindex}")
def get_product_by_size(product_size: str, number: int, startindex: int):
    """
    Get multiple products with their images based on the provided product size.

    Parameters:
    - product_size: The size of the product.
    - number: The maximum number of products to fetch.
    - startindex: The starting index of the products to fetch.

    Returns:
    - A list of products with their images.
    """
    # Call the helper function to execute the query and return the result
    query = filter_products_helper.search_product_by_productsize(session=session, product_size=product_size, number=number, startindex=startindex)
    # Get the data using the helper function
    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data


@router.get("/filterbyprice/{min_price}/{max_price}/{number}/{product_name}/{startindex}")
def filter_by_price(min_price: float, max_price: float, number: int, product_name: str, startindex: int):
    """
    Get multiple products with their images based on the provided price range and product name.

    Parameters:
    - min_price: The minimum price of the product.
    - max_price: The maximum price of the product.
    - number: The maximum number of products to fetch.
    - product_name: The name of the product.
    - startindex: The starting index of the products to fetch.

    Returns:
    - A list of products with their images.
    """
    # Call the helper function to execute the query and return the result
    query = filter_products_helper.filterbyprice(session=session, min_price=min_price, max_price=max_price, number=number, product_name=product_name, startindex=startindex)

    # Get the data using the helper function
    data = filter_products_helper.helper_for_filters(session=session, query=query)
    return data
