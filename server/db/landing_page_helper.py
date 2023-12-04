from server.models.models1 import session
from server.models.models import ProductImage, Review, UserPurchase, Product, Sales
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy import func, select


def get_random_products_helper(number_of_products: int):
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

    return query



def get_top_rated_products_helper(number_of_products: int = 5):
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
        .filter(review_info_subquery.c.num_reviews > 0)  # Only include products with reviews
        .order_by(desc(review_info_subquery.c.avg_rating), desc(review_info_subquery.c.num_reviews))
        .distinct(review_info_subquery.c.avg_rating, review_info_subquery.c.num_reviews, Product.id)  # Ensure distinct products in the result
        .limit(number_of_products)
    )

    return query