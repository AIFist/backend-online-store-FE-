from fastapi.routing import APIRouter
from server.models.models1 import session
from server.db import landing_page_helper 
from server.utils import helper_for_getting_data
from server.utils.rate_limit import rate_limited
from server.schemas import landing_page_schemas
from typing import List
from fastapi import  status, Request

router = APIRouter(prefix="/landingpage", tags=["landing page Endpoints"])

# Your endpoint function
@router.get("/getrandomproducts/{number_of_products}",
            status_code=status.HTTP_200_OK,
            response_model=List[landing_page_schemas.LandingPageProductCResponse]
          )
@rate_limited(max_calls=10, time_frame=60)
async def get_random_products(request: Request, number_of_products: int):  # Reordered arguments
    """
    Get a random subset of products for the landing page.
    
    Args:
        request (Request): FastAPI Request object.
        number_of_products (int): The number of products to retrieve.

    Returns:
        List: A list of dictionaries containing product information.
    """
    print(number_of_products)
    query = landing_page_helper.get_random_products_helper(number_of_products=number_of_products)

    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data



# need to change the the way it retrun the result
@router.get("/gettrendingproducts/{number_of_products}", 
            status_code=status.HTTP_200_OK,
            response_model=List[landing_page_schemas.LandingPageUpToGivenNumberResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_trending_products_with_reviews(request: Request,number_of_products:int):
    """
    Note: This endpoint returns different data from the other endpoints.
    and there is issue in this endpoint which is for some reason it just return one images object

    This endpoint is in progress.

    Args:
        number_of_products (_type_): _description_
    """
    query = landing_page_helper.get_trending_product_with_reviews(number_of_products=number_of_products)
    
    # data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    # return data
    result = session.execute(query).all()
    return result


@router.get("/gettopratedproducts/{number_of_products}",
            status_code=status.HTTP_200_OK,
            response_model=List[landing_page_schemas.LandingPageProductCResponse]
            )
@rate_limited(max_calls=10, time_frame=60)
async def get_top_rated_products(request: Request, number_of_products: int):
    """
    Get the top rated products.

    Args:
        number_of_products (int): The number of products to retrieve.

    Returns:
        data (List[dict]): A list of dictionaries representing the top rated products.
    """
    # Call the helper function to get the query for retrieving top rated products
    query = landing_page_helper.get_top_rated_products_helper(number_of_products=number_of_products)
    # result = session.execute(query).all()
    # return result
    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data
