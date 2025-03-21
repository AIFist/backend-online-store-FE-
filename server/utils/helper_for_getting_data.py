from fastapi import HTTPException
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

def helper_for_filters_with_review_and_discount(session, query):
    """
    Helper function to execute a query and extract product details with images and reviews.
    Args:
        session (Session): The database session to execute the query.
        query (Query): The query to execute.
    Returns:
        list: A list of dictionaries containing product details with images and reviews.
    """
    try:
        # Execute the query and get the results
        result = session.execute(query).all()

        if not result:
            raise HTTPException(status_code=404, detail="Products not found")

        # Extract the Product, ProductImage, number of reviews, and average rating from the result
        products_with_images_and_reviews = [
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
                "discount_percent": avg_discount_percent,
                "category_name": category_name,
            }
            for product, image,category_name, num_reviews, avg_rating, avg_discount_percent in result
        ]

        return products_with_images_and_reviews
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")    

def helper_for_getting_data_tranding(session, query):
    """
    Helper function to execute a query and extract product details with images and reviews.
    Args:
        session (Session): The database session to execute the query.
        query (Query): The query to execute.
    Returns:
        list: A list of dictionaries containing product details with images and reviews.
    """
    try:
        # Execute the query and get the results
        result = session.execute(query).all()

        if not result:
            raise HTTPException(status_code=404, detail="Products not found")
        # Extract the Product, ProductImage, number of reviews, average rating, and purchase count from the result
        products_with_images_and_reviews = [
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
                "discount_percent": avg_discount_percent,
                "purchase_count": purchase_count  # Include the purchase count in the result
            }
            for product, image, num_reviews, avg_rating, avg_discount_percent, purchase_count in result
        ]
        return products_with_images_and_reviews
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def helper_get_featured_products(session, query):
    """
    Retrieves and organizes featured products with their images from the database.

    Args:
        session: The session to execute the query.
        query: The query to retrieve the featured products.

    Returns:
        A list of dictionaries representing the featured products with their images.
    """
    try:
        result = session.execute(query).all()

        # Use defaultdict to organize products with their images
        products_dict = defaultdict(lambda: {"Product": None, "ProductImages": [], "num_reviews": 0, "avg_rating": None, "rownum": None, "discount_percent": None, "category_name": None})

        for row in result:
            product_id = row.Product.id
            if not products_dict[product_id]["Product"]:
                products_dict[product_id]["Product"] = row.Product

            # Append each image to the ProductImages list
            products_dict[product_id]["ProductImages"].append({"id": row.ProductImage.id, "product_id": product_id, "image_path": row.ProductImage.image_path})

            # Sum up the reviews and calculate the average rating
            products_dict[product_id]["num_reviews"] += row.num_reviews
            if row.avg_rating is not None:
                products_dict[product_id]["avg_rating"] = row.avg_rating

            # Save the rownum for each product
            products_dict[product_id]["rownum"] = row.rownum
            products_dict[product_id]["discount_percent"] = row.latest_discount_percent
            products_dict[product_id]["category_name"] = row.category_name

        # Convert the dictionary values to a list of results
        final_result = [result for result in products_dict.values()]

        return final_result
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
