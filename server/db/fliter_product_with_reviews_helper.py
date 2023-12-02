from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage, Review
from sqlalchemy import func, select, outerjoin

def get_products_with_images_and_reviews(product_name, startindex, number):
    # Create the main query
    query = (
    select(
        Product,
        ProductImage,
        func.count(Review.id).label("num_reviews"),
        func.avg(Review.rating).label("avg_rating")
    )
    .outerjoin(ProductImage)
    .outerjoin(Review)
    .filter(Product.product_name.contains(product_name))
    .offset(startindex)
    .limit(number)
    .group_by(Product, ProductImage)
    .order_by(Product.id)
    .distinct(Product.id)
    )
    return query

def get_products(number: int, startindex: int):
    """
    Retrieves a list of products with their corresponding images.

    Args:
        session: The database session to use.
        number: The maximum number of products to retrieve.
        startindex: The index of the first product to retrieve.

    Returns:
        A query object that can be executed to retrieve the products and their images.
    """
    # Create the main query to retrieve products and their images
    query = (
    select(
        Product,
        ProductImage,
        func.count(Review.id).label("num_reviews"),
        func.avg(Review.rating).label("avg_rating")
    )
    .outerjoin(ProductImage)
    .outerjoin(Review)
    .offset(startindex)
    .limit(number)
    .group_by(Product, ProductImage)
    .order_by(Product.id)
    .distinct(Product.id)
    )
    return query

def get_product_by_category(category_id,startindex, number):
    query = (
    select(
        Product,
        ProductImage,
        func.count(Review.id).label("num_reviews"),
        func.avg(Review.rating).label("avg_rating")
    )
    .outerjoin(ProductImage)
    .outerjoin(Review)
    .filter(Product.category_id == category_id)
    .offset(startindex)
    .limit(number)
    .group_by(Product, ProductImage)
    .order_by(Product.id)
    .distinct(Product.id)
    )
    return query
