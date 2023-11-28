
from fastapi import HTTPException
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage


def helper_for_get_request(session, query, count_subquery, number):
    # Check if the number of rows in the table is less than the specified number
    if session.execute(select([func.count()]).select_from(query.alias())).scalar() < number:
        query = query.limit(count_subquery)  # Limit the main query by the count
        
    # Execute the query and get the results
    result = session.execute(query).all()
    # Execute the query and get the first result
    # If no result is found, raise an HTTPException with a 404 status code
    if result is None:
        raise HTTPException(status_code=404, detail=f"Product not found")
    # Extract the Product and ProductImage from the result
    products_with_images = []
    for product, image in result:
        product_with_images = {
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
        products_with_images.append(product_with_images)

    return products_with_images

def helper_for_get_one_product(session, id:int):
    # Create a query to select the Product and ProductImage based on the provided ID
    query = (
        select(Product, ProductImage)
        .join(ProductImage)
        .filter(Product.id == id)
        .order_by(Product.id)
    )
    # Execute the query and get the first result
    result = session.execute(query).first()
    # If no result is found, raise an HTTPException with a 404 status code
    if result is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

    # Extract the Product and ProductImage from the result
    product, image = result

    # Create a dictionary to store the product information
    product_with_images = {
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
        "images": [],
    }

    # If there is an image, add it to the product_with_images dictionary
    if image is not None:
        product_with_images["images"].append({
            "image_path": image.image_path,
        })
    
    # Return the product_with_images dictionary
    return product_with_images
    