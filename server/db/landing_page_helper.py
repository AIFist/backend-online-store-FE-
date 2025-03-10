from server.models.models1 import session
from server.models.models import ProductImage, Review, UserPurchase, Product, Sales, ProductCategory
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy import func, select, distinct


def get_random_products_helper(number_of_products: int):
    """
    Retrieve a random subset of product details.
    Args:
        number_of_products: The number of random product details to retrieve.
    Returns:
        The query that retrieves the random subset of product details.
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
            ProductCategory.category_name,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(Sales)
        .outerjoin(ProductCategory, product_alias.category_id == ProductCategory.id)  # Use product_alias here
        .filter(product_alias.id == random_product_ids.c.id)  # Use product_alias here
        .group_by(product_alias, ProductImage, ProductCategory.category_name, Sales.discount_percent)
        .order_by(product_alias.id)
        .distinct(product_alias.id)
    )


    return query


def get_top_rated_products_helper(number_of_products: int = 5):
    """
    Retrieve top rated products with reviews and discounts.
    Args:
        number_of_products (int): Number of products to retrieve. Defaults to 5.
    Returns:
        sqlalchemy.sql.selectable.Select: SQLAlchemy select query to retrieve top rated products.
    """
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
            ProductCategory.category_name,
            review_info_subquery.c.num_reviews,
            review_info_subquery.c.avg_rating,
            Sales.discount_percent.label("latest_discount_percent")
        ])
        .select_from(Product)  # Explicitly set the main table
        .outerjoin(ProductImage)
        .outerjoin(review_info_subquery, Product.id == review_info_subquery.c.id)
        .outerjoin(Sales, Product.id == Sales.product_id)
        .outerjoin(ProductCategory, Product.category_id == ProductCategory.id)  # Add this line for the missing join condition
        .filter(review_info_subquery.c.num_reviews > 0)
        .order_by(desc(review_info_subquery.c.avg_rating), desc(review_info_subquery.c.num_reviews))
        .distinct(review_info_subquery.c.avg_rating, review_info_subquery.c.num_reviews, Product.id)
        .limit(number_of_products)
    )

    return query


# purchase_counts_subquery not wokring properly
def get_trending_product_with_reviews(number_of_products: int):
    """
    Retrieves a list of trending products with reviews and discounts.
    Args:
        number_of_products (int): The number of products to retrieve.
    Returns:
        query: The query object containing the results.
    """

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

    # Create a subquery to get the count of purchases for each product
    purchase_counts_subquery = (
        select([UserPurchase.product_id, func.count(UserPurchase.id).label("purchase_count")])
        .group_by(UserPurchase.product_id)
    ).alias("purchase_counts")

    # Create the main query to retrieve product details with reviews and discounts

    query = (
        select([
            Product,
            ProductImage,
            ProductCategory.category_name,
            review_info_subquery.c.num_reviews.label("num_reviews"),
            review_info_subquery.c.avg_rating.label("avg_rating"),
            Sales.discount_percent.label("discount_percent"),
            purchase_counts_subquery.c.purchase_count.label("purchase_count")
        ])
        .select_from(Product)
        .outerjoin(ProductImage)
        .outerjoin(review_info_subquery, Product.id == review_info_subquery.c.id)
        .outerjoin(Sales, Product.id == Sales.product_id)
        .outerjoin(purchase_counts_subquery, Product.id == purchase_counts_subquery.c.product_id)
        .outerjoin(ProductCategory, Product.category_id == ProductCategory.id)  # Add this line for the missing join condition
        .filter(review_info_subquery.c.num_reviews > 0)
        .order_by(
            desc(review_info_subquery.c.num_reviews),
            desc(purchase_counts_subquery.c.purchase_count),
            desc(review_info_subquery.c.avg_rating)
        )
        .distinct(review_info_subquery.c.avg_rating, review_info_subquery.c.num_reviews, purchase_counts_subquery.c.purchase_count, Product.id)
        .limit(number_of_products)
    )
    return query
