from fastapi.routing import APIRouter
from server.models.models1 import session
from server.db import fliter_product_with_reviews_helper
from server.utils import helper_for_getting_data
from typing import List
from fastapi import  status, HTTPException, Request
from server.schemas import filter_products_schemas
from sqlalchemy.exc import SQLAlchemyError
from server.utils.rate_limit import rate_limited


router = APIRouter(prefix="/productfilter", tags=["------------------------neutral Auth ----------------------Filters for Product Endpoints"])


@router.get("/getbyname/{search_keyword}/{number}/{startindex}", 
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_by_name(request: Request, search_keyword: str, number: int, startindex: int):
    """
    Get multiple products with their images based on the provided product name.

    Args:
    - product_name (str): The name of the product.
    - number (int): The number of products to retrieve.
    - startindex (int): The starting index for retrieving the products.

    Returns:
        dict: A dictionary containing the products and their images.
    """
    query = fliter_product_with_reviews_helper.get_products_with_images_and_reviews(search_keyword=search_keyword, number=number, startindex=startindex)

    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data


@router.get("/getproducts/{number}/{startindex}",
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_up_to_given_number(request: Request,number: int, startindex: int):
    """
    Get a list of products with their images up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.
    - startindex: The starting index of the rows to retrieve.

    Returns:
    - List of products with images.
    """

    query = fliter_product_with_reviews_helper.get_products(number=number, startindex=startindex)
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data
    # return result


@router.get("/getbycategory/{category_id}/{number}/{startindex}",
            status_code= status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_by_category(request: Request,category_id: int, number: int, startindex: int):
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
    query = fliter_product_with_reviews_helper.get_product_by_category(category_id=category_id, number=number, startindex=startindex)
    # Get the data using the helper function
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data

 # this function retruns 404 even if product  are in the database

@router.get("/getbycategory_keyword/{category_id}/{search_keyword}/{number}/{startindex}", 
            status_code= status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_by_keyword(request: Request,category_id: int, search_keyword: str, number: int, startindex: int):
    """
    Note: The search keyword is working product name 
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
    query = fliter_product_with_reviews_helper.get_product_by_category_keyword(category_id=category_id, search_keyword=search_keyword, number=number, startindex=startindex)

    # Get the data using the helper function
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data

@router.get("/searchbyproductsize/{product_size}/{number}/{startindex}",
            status_code=status.HTTP_200_OK,
            # response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_product_by_size(request: Request,product_size: str, number: int, startindex: int):
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
    query = fliter_product_with_reviews_helper.search_product_by_productsize(product_size=product_size, number=number, startindex=startindex)
    # Get the data using the helper function
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data


@router.get("/filterbyprice/{min_price}/{max_price}/{number}/{product_name}/{startindex}",
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FilterProductsProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def filter_by_price(request: Request, min_price: float, max_price: float, number: int, product_name: str, startindex: int):
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
    query = fliter_product_with_reviews_helper.filter_product_by_price(min_price=min_price, max_price=max_price, number=number, product_name=product_name, startindex=startindex)

    # Get the data using the helper function
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data

# Get featured products need responde model
@router.get("/getfeaturedproducts/{number}/{startindex}",
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.FeaturedProductUpToGivenNumberResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_featured_product_up_to_given_number(request: Request,number: int, startindex: int):
    """
    Note: This endpoint returns different data from the other endpoints.
    Get a list of products with their images up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.
    - startindex: The starting index of the rows to retrieve.

    Returns:
    - List of products with images.
    """
    # Get the query to retrieve featured products
    query = fliter_product_with_reviews_helper.get_featured_products(number=number, startindex=startindex)

    # Get the data using the helper function
    result =helper_for_getting_data.helper_get_featured_products(session= session, query=query)
    # result = session.execute(query).all()
    return result


@router.get("/dealoftheday/{number}",
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.ProductForNewArrivalesResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def deal_of_the_day(request: Request, number: int):
    """
    Get a list of products who has highest sales with their images up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.
    - startindex: The starting index of the rows to retrieve.

    Returns:
    - List of products with images.
    """

    product_ids = fliter_product_with_reviews_helper.deal_of_the_day(session=session,number=number)
    query = fliter_product_with_reviews_helper.get_product_details_query(product_ids)

    try:
        # Execute the query and retrieve the results
        result = session.execute(query).all()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Reverse the order of the results
    re = result[::-1]

    return re


@router.get("/newarrivals/{number}",
            status_code=status.HTTP_200_OK,
            response_model=List[filter_products_schemas.ProductForNewArrivalesResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def new_arrivales(request: Request, number: int):
    """
    Get a list of products with the highest sales up to the specified number.

    Parameters:
    - number: The maximum number of rows to retrieve.

    Returns:
    - A list of products with images.
    """

    # Get the product ids of the new arrivals
    product_ids = fliter_product_with_reviews_helper.new_arrivals(session=session, number=number)

    # Generate the query to get the details of the products
    query = fliter_product_with_reviews_helper.get_product_details_query(product_ids)

    try:
        # Execute the query and retrieve the results
        result = session.execute(query).all()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Reverse the order of the results
    re = result[::-1]

    return re
