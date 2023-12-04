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
    query = landing_page_helper.get_random(number_of_products=number_of_products)
    

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
    try:
        # Use aliased to create an alias for the Review table
        review_alias = aliased(Review)

        # Create a subquery to get the number of reviews and average rating for each product
        review_info_subquery = (
            select([
                Product.id,
                func.count(review_alias.id).label("num_reviews"),
                func.avg(review_alias.rating).label("avg_rating")
            ])
            .outerjoin(review_alias)
            .group_by(Product.id)
        ).alias("review_info")

        # Create the main query to retrieve product details with reviews and discounts
        query = (
            select([
                Product,
                ProductImage,
                review_info_subquery.c.num_reviews,
                review_info_subquery.c.avg_rating,
                Sales.discount_percent.label("latest_discount_percent")
            ])
            .select_from(Product)  # Explicitly set the main table
            .outerjoin(ProductImage)
            .outerjoin(review_info_subquery, Product.id == review_info_subquery.c.id)
            .outerjoin(Sales, Product.id == Sales.product_id)
            .order_by(desc(review_info_subquery.c.avg_rating))
            .limit(number_of_products)
        )

        # Execute the query and fetch the result
        result = session.execute(query).all()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        # Handle the error or log it as needed
        return {"error": "Internal Server Error"}

    # Extract the product details from the result
    top_rated_products = [
        {
            "id": product.id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "product_size": product.product_size,
            "SKU": product.SKU,
            "target_audience": product.target_audience,
            "product_color": product.product_color,
            "created_at": product.created_at,
            "category_id": product.category_id,
            "images": [{"id": image.id, "image_path": image.image_path} for image in product.images],
            "num_reviews": num_reviews,
            "avg_rating": avg_rating,
            "latest_discount_percent": latest_discount_percent,
        }
        for product, image, num_reviews, avg_rating, latest_discount_percent in result
    ]

    return top_rated_products