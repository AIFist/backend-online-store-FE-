from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage, Review
from sqlalchemy import func, select
from sqlalchemy import or_

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

def get_product_by_category(category_id: int,startindex: int, number: int):
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


def get_product_by_category_keyword(category_id: int, search_keyword: str, number: int, startindex: int):
    query = (
    select(
        Product,
        ProductImage,
        func.count(Review.id).label("num_reviews"),
        func.avg(Review.rating).label("avg_rating")
    )
    .outerjoin(ProductImage)
    .outerjoin(Review)
    .filter(or_(Product.product_name.contains(search_keyword), Product.description.contains(search_keyword)))
    .filter(Product.category_id == category_id)
    .offset(startindex)
    .limit(number)
    .group_by(Product, ProductImage)
    .order_by(Product.id)
    .distinct(Product.id)
)

    return query

def search_product_by_productsize(product_size: str, number: int, startindex: int):
    """
    Search products by product size and return a query object.
    Args:
        session: The database session.
        product_size: The size of the product to search for.
        number: The number of products to retrieve.
        startindex: The starting index for retrieving products.
    Returns:
        A query object that fetches products filtered by product size.
    """
    # Call the helper function to execute the query and return the result
    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .filter(Product.product_size.contains(product_size))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query

def filter_product_by_price(min_price: float, max_price: float, number: int, product_name: str, startindex: int):
    """
    Filter products by price range and return a query object.
    Args:
        session: The database session.
        min_price: The minimum price of the product to filter by.
        max_price: The maximum price of the product to filter by.
        number: The number of products to retrieve.
        product_name: The name of the product to filter by.
        startindex: The starting index for retrieving products.
    Returns:
        A query object that fetches products filtered by price range.
    """
    # Call the helper function to execute the query and return the result
    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .filter(Product.price >= min_price)
        .filter(Product.price <= max_price)
        .filter(Product.product_name.contains(product_name))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query