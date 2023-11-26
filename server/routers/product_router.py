from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas

router = APIRouter(prefix="/product", tags=["Product  CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)


async def create_product(product_data: product_schemas.ProductCreate = Body(...)):
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
    Delete a product for product table by ID.

    Parameters:
    - id: ID of the product  to be deleted.
    - session: SQLAlchemy Session dependency.

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
    Update a product  by ID.

    Parameters:
    - id: ID of the product  to be updated.
    - prouctcat_update: ProductUpdate model from product_cat_schemas containing updated data.
    - session: SQLAlchemy Session dependency.

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