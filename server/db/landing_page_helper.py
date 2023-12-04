from server.models.models1 import session
from server.models.models import ProductImage, Review, UserPurchase, Product, Sales
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import aliased
from sqlalchemy import func, select


def get_random(number_of_products: int):
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