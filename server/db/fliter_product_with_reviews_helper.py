from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import func, select
from server.models.models import Product, ProductImage, Review, Sales, FeaturedProduct
from sqlalchemy import func, select
from sqlalchemy import or_, and_



def get_products_with_images_and_reviews(product_name, startindex, number):
    """
    Get products with images and reviews.
    Args:
        product_name (str): The name of the product to search for.
        startindex (int): The starting index to retrieve the products.
        number (int): The number of products to retrieve.
    Returns:
        Query: The SQLAlchemy query object.
    """
    # Create the main query
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(Product.product_name.ilike(f'%{product_name}%'))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query

def get_products(number: int, startindex: int):
    """
    Retrieves a list of products with their corresponding images.

    Args:
        number: The maximum number of products to retrieve.
        startindex: The index of the first product to retrieve.

    Returns:
        A query object that can be executed to retrieve the products and their images.
    """
    # Create the main query to retrieve products and their images
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )
    return query

def get_product_by_category(category_id: int,startindex: int, number: int):
    """
    Retrieve products by category with additional information:
    - ProductImage
    - Number of reviews
    - Average rating
    Args:
    - category_id: int - the ID of the category
    - startindex: int - the starting index for pagination
    - number: int - the number of products to retrieve
    Returns:
    - query: SQLAlchemy query object
    """
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(Product.category_id == category_id)
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query


def get_product_by_category_keyword(category_id: int, search_keyword: str, number: int, startindex: int):
    """
    Retrieve products based on category, search keyword, and pagination.
    Args:
        category_id (int): The ID of the category to filter the products by.
        search_keyword (str): The keyword to search for in the product name and description.
        number (int): The number of products to retrieve.
        startindex (int): The starting index of the retrieved products.
    Returns:
        sqlalchemy.orm.query.Query: The query object to retrieve the products.
    """
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(or_(Product.product_name.ilike(f'%{search_keyword}%')), Product.description.ilike(f'%{search_keyword}%'))
        .filter(Product.category_id == category_id)
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query


def search_product_by_productsize(product_size: str, number: int, startindex: int):
    """
    Search products by product size and return a query object.
    Args:
        product_size: The size of the product to search for.
        number: The number of products to retrieve.
        startindex: The starting index for retrieving products.
    
    Returns:
        A query object that fetches products filtered by product size.
    """
    # Call the helper function to execute the query and return the result
    
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(Product.product_size.ilike(f'%{product_size}%'))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    return query

def filter_product_by_price(min_price: float, max_price: float, number: int, product_name: str, startindex: int):
    """
    Filter products by price range and return a query object.
    Args:
        min_price: The minimum price of the product to filter by.
        max_price: The maximum price of the product to filter by.
        number: The number of products to retrieve.
        product_name: The name of the product to filter by.
        startindex: The starting index for retrieving products.
    Returns:
        A query object that fetches products filtered by price range.
    """
    # Create the query object
    
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            Sales.discount_percent.label("latest_discount_percent")
        )
        .outerjoin(ProductImage)
        .outerjoin(Review)
        .outerjoin(subquery, and_(Product.id == subquery.c.product_id))
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(Product.price >= min_price)
        .filter(Product.price <= max_price)
        .filter(Product.product_name.ilike(f'%{product_name}%'))
        .offset(startindex)
        .limit(number)
        .group_by(Product, ProductImage, Sales.discount_percent)
        .order_by(Product.id)
        .distinct(Product.id)
    )


    return query

def get_featured_products(number: int, startindex: int):
    """
    Retrieves a list of featured products with additional information.

    Args:
        number (int): The number of products to retrieve.
        startindex (int): The starting index of the products.

    Returns:
        sqlalchemy.sql.selectable.Select: The query to retrieve the featured products.
    """
    # Create a common table expression (CTE) to rank the featured products
    cte = (
        select(
            FeaturedProduct.product_id,
            func.row_number().over().label("rownum")
        )
        .select_from(FeaturedProduct)
        .alias("ranked_featured")
    )

    # Create a subquery to get the latest discount percent for each product
    subquery = (
        select(
            Sales.product_id,
            func.max(Sales.sale_date).label("max_sale_date")
        )
        .group_by(Sales.product_id)
        .alias("latest_sales")
    )

    # Build the query to retrieve the featured products with additional information
    query = (
        select(
            Product,
            ProductImage,
            func.count(Review.id).label("num_reviews"),
            func.avg(Review.rating).label("avg_rating"),
            cte.c.rownum,
            Sales.discount_percent.label("latest_discount_percent")
        )
        .select_from(Product)
        .join(cte, Product.id == cte.c.product_id)
        .outerjoin(ProductImage, Product.id == ProductImage.product_id)
        .outerjoin(Review, Product.id == Review.product_id)
        .outerjoin(subquery, Product.id == subquery.c.product_id)
        .outerjoin(Sales, and_(Product.id == Sales.product_id, Sales.sale_date == subquery.c.max_sale_date))
        .filter(cte.c.rownum.between(startindex, startindex + number - 1))
        .group_by(Product, ProductImage, cte.c.rownum, Sales.discount_percent)
        .order_by(cte.c.rownum)
    )

    return query
