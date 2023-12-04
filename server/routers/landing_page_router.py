from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import ProductImage, Review, UserPurchase, Product, Sales
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from server.db import landing_page_helper 
from server.utils import helper_for_getting_data

router = APIRouter(prefix="/landingpage", tags=["landing page Endpoints"])

@router.get("/getrandomproducts/{number_of_products}")
def get_random_products(number_of_products):
    """
    Get a random subset of products for the landing page.
    
    Args:
        number_of_products (int): The number of products to retrieve.

    Returns:
        List: A list of dictionaries containing product information.
    """
    query = landing_page_helper.get_random_products_helper(number_of_products=number_of_products)

    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data


@router.get("/gettrendingproducts/{number_of_products}")
def get_trending_products_with_reviews(number_of_products):
    """
    This endpoint is in progress.

    Args:
        number_of_products (_type_): _description_
    """
    pass


@router.get("/gettopratedproducts/{number_of_products}")
def get_top_rated_products(number_of_products: int):
    
    query = landing_page_helper.get_top_rated_products_helper(number_of_products=number_of_products)

    data = helper_for_getting_data.helper_for_filters_with_review_and_discount(session=session, query=query)
    return data