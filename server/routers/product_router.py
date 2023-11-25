from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product, ProductImage
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas

router = APIRouter(prefix="/product", tags=["Product  CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)

def create_product(product_data: product_schemas.ProductCreate = Body(...)):
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