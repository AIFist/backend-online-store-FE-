from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas
from sqlalchemy import select
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
            session.close()  # 

    return new_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int,):
    """
    Delete a product by ID.

    Parameters:
    - id: ID of the product to be deleted.
    - db: SQLAlchemy Session dependency.

    Returns:
    - Response with 204 status code if successful.
    """
    try:
        product_query = session.query(Product).filter(Product.id == id)
        product = product_query.first()
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product Category with id {id} does not exist")
        
        product_query.delete(synchronize_session=False)
        session.commit()
    
    except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()  # Rollback the transaction

    finally:
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
        Product_query = session.query(Product).filter(Product.id == id)
        db_product = Product_query.first()
        if db_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {id} does not exist")
        
        
        Product_query.update(product_update.model_dump(), synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()  # Rollback the transaction

    finally:
            session.close()
    return Product_query.first()

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
    
    results = session.execute(query).fetchall()

    # Create a dictionary to store products with their images
    products_with_images = {}

    for product, image in results:
        if product.id not in products_with_images:
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
    query = (
        select(Product, ProductImage)
        .join(ProductImage)
        .filter(Product.id == id)
        .order_by(Product.id)
    )
    result = session.execute(query).first()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

    product, image = result
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

    if image is not None:
        product_with_images["images"].append({
            "image_path": image.image_path,
        })

    return product_with_images
    
