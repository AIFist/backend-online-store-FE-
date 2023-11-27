from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas
from sqlalchemy import select
from sqlalchemy import func, select, outerjoin
router = APIRouter(prefix="/product", tags=["Product  CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: product_schemas.ProductCreate = Body(...)):
    """
    Create a new product along with associated images.
    
    Parameters:
    - product_data: Pydantic model containing product details.
    
    Returns:
    - Created Product.
    """
    
    try:
        # Convert the Pydantic model to a SQLAlchemy model
        new_product = Product(**product_data.model_dump(exclude={"images"}))

        # Create product images and associate with the product
        for image_data in product_data.images:
            image = ProductImage(**image_data.model_dump())
            new_product.images.append(image)

        # Add the product to the session and commit
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        session.close()

    return new_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.

    Returns:
    - Response with 204 status code if successful.
    """
    try:
        # Query the product with the given id
        product_query = session.query(Product).filter(Product.id == id)
        product = product_query.first()

        # If product does not exist, raise 404 error
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")

        # Delete the product
        product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy errors
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction

    finally:
        # Close the session
        session.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a product 
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_product(id: int, product_update: product_schemas.ProductUpadte = Body(...)):
    """
    Update a product by ID.

    Parameters:
    - id: ID of the product to be updated.
    - product_update: Pydantic model containing updated data.

    Returns:
    - Updated Product.
    """
    try:
        # Retrieve the product from the database based on the provided ID
        product_query = session.query(Product).filter(Product.id == id)
        db_product = product_query.first()
        if db_product is None:
            # If the product does not exist, raise an HTTP 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")

        # Update the product with the new data
        product_query.update(product_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        # If an error occurs during the update, print the error and rollback the transaction
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        # Close the database session
        session.close()

    # Return the updated product
    return product_query.first()

@router.get("/all")
async def get_all_products():
    """
    Get all products with their images.

    Parameters:
    - db: SQLAlchemy Session dependency.

    Returns:
    - List of products with images.
    """
    # Use a join query to retrieve products with their images
    query = (
        select(Product, ProductImage)
        .join(ProductImage)
        .order_by(Product.id)
    )
    
    # Execute the query and fetch all results
    results = session.execute(query).fetchall()

    # Create a dictionary to store products with their images
    products_with_images = {}

    # Iterate through the results and populate the dictionary
    for product, image in results:
        if product.id not in products_with_images:
            # Create a new dictionary for the product if it doesn't exist
            products_with_images[product.id] = {
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
        
        if image is not None:
            # Append the image to the product's images list
            products_with_images[product.id]["images"].append({
                "image_path": image.image_path,
            })

    # Convert the dictionary values to a list for response
    result_list = list(products_with_images.values())
    
    return result_list

@router.get("/{id}")
async def get_one_product(id: int):
    """
    Get a single product with its images based on the provided product ID.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - Product with images.
    """
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
    

@router.get("getproducts/{numer}")
async def get_product_up_to_given_number(number: int):
    """
    Get a list of products with their images based on the provided number of rows you want.

    Parameters:
    - id: Product ID obtained from the path parameter.

    Returns:
    - List of products with images.
    """
    # Create a subquery to count the rows
    count_subquery = (
        select([func.count()])
        .select_from(outerjoin(Product, ProductImage))
        .scalar_subquery()
    )

    # Create the main query
    query = (
        select(Product, ProductImage)
        .outerjoin(ProductImage)
        .limit(number)
        .order_by(Product.id)
        .distinct(Product.id)
    )

    # Check if the number of rows in the table is less than the specified number
    if session.execute(select([func.count()]).select_from(query.alias())).scalar() < number:
        query = query.limit(count_subquery)  # Limit the main query by the count

    # Execute the query and get the results
    results = session.execute(query).all()
        
    # If no result is found, raise an HTTPException with a 404 status code
    if not results:
        raise HTTPException(status_code=404, detail=f"No products found up to the given number {number}")

    # Extract the results and create a list of products with images
    products_with_images = []
    for product, image in results:
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