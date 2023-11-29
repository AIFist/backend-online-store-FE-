from fastapi import HTTPException, status,Response
from sqlalchemy import func, select, select
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas

def helper_for_filters(session, query):
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
