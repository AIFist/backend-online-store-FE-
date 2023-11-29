from fastapi import HTTPException
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage
from sqlalchemy import func, select, outerjoin

def helper_for_filters(session, query):
    """
    Helper function to execute a query and return products with images
    
    Args:
        session: the database session object
        query: the query to execute
        
    Returns:
        products_with_images: a list of products with their images
    """
    # Execute the query and get the results
    result = session.execute(query).all()

    if not result:
        raise HTTPException(status_code=404, detail="Products not found")

    # Extract the Product and ProductImage from the result
    products_with_images = [
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
        }
        for product, image in result
    ]

    return products_with_images

def get_products(session, number: int, startindex: int):
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
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows in the table
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the total number of rows is less than the specified number
    if total_rows < number:
        # Limit the query to the total number of rows
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .offset(startindex)
            .limit(total_rows)
            .order_by(Product.id)
            .distinct(Product.id)
        )
        
    return query

def get_product_by_name(session, product_name:str, number: int, startindex: int):
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.product_name.contains(product_name))
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the number of rows in the table is less than the specified number
    if total_rows < number:
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .filter(Product.product_name.contains(product_name))
            .offset(startindex)
            .limit(total_rows)  # Limit the query to the total number of rows
            .order_by(Product.id)
            .distinct(Product.id)
        )

    return query

def get_product_by_category(session, category_id: int, number: int, startindex: int):
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.category_id == category_id)
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the number of rows in the table is less than the specified number
    if total_rows < number:
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .filter(Product.category_id == category_id)
            .offset(startindex)  # Start from the specified index
            .limit(total_rows)  # Limit the query to the total number of rows
            .order_by(Product.id)
            .distinct(Product.id)
        )

    return query

def get_product_by_category_keyword(session, category_id: int, search_keyword: str, number: int, startindex: int):
    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.category_id == category_id)
        .filter(Product.product_name.contains(search_keyword))
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the number of rows in the table is less than the specified number
    if total_rows < number:
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .filter(Product.category_id == category_id)
            .filter(Product.product_name.contains(search_keyword))
            .offset(startindex)
            .limit(total_rows)  # Limit the query to the total number of rows
            .order_by(Product.id)
            .distinct(Product.id)
        )

    return query

def search_product_by_productsize(session, product_size: str, number: int, startindex: int):
    # Call the helper function to execute the query and return the result
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.product_size.contains(product_size)) 
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the number of rows in the table is less than the specified number
    if total_rows < number:
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .filter(Product.product_size.contains(product_size)) 
            .offset(startindex)
            .limit(total_rows)  # Limit the query to the total number of rows
            .order_by(Product.id)
            .distinct(Product.id)
        )

    return query

def filterbyprice(session, min_price: float, max_price: float, number: int, product_name: str, startindex: int):
    # Call the helper function to execute the query and return the result
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .filter(Product.product_name.contains(product_name))  # Filter by product name
        .filter(Product.price >= min_price)  # Filter by minimum price
        .filter(Product.price <= max_price)
        .offset(startindex)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Count the total number of rows
    total_rows = session.execute(select([func.count()]).select_from(outerjoin(Product, ProductImage))).scalar()

    # Check if the number of rows in the table is less than the specified number
    if total_rows < number:
        query = (
            select(Product, ProductImage)
            .outerjoin(ProductImage)
            .filter(Product.product_name.contains(product_name))  # Filter by product name
            .filter(Product.price >= min_price)  # Filter by minimum price
            .filter(Product.price <= max_price)
            .offset(startindex)
            .limit(total_rows)  # Limit the query to the total number of rows
            .order_by(Product.id)
            .distinct(Product.id)
        )

    return query