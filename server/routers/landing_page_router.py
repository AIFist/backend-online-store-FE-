from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import ProductImage, Review, UserPurchase, Product, Sales
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError


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
    # Use aliased to create an alias for the Product table
    product_alias = aliased(Product)

    # Create a subquery to get a random subset of product IDs
    random_product_ids = (
        select([Product.id])
        .order_by(func.random())
        .limit(number_of_products)
    ).alias("random_products")

    # Create the main query to retrieve product details for the random subset
    query = (
        select(
            product_alias,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(Sales)
        .filter(product_alias.id == random_product_ids.c.id)
        .group_by(product_alias, ProductImage, Sales.discount_percent)
        .order_by(product_alias.id)
        .distinct(product_alias.id)
    )

    # Execute the query and fetch the result
    result = session.execute(query).all()

    # Extract the product details from the result
    products = [
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

    return products


@router.get("/gettrendingproducts/{number_of_products}")
def get_trending_products_with_reviews(number_of_products):
    """
    This endpoint is in progress.

    Args:
        number_of_products (_type_): _description_
    """
    pass