from fastapi import Body, status,HTTPException, Response
from fastapi.routing import APIRouter
from server.models.models1 import session
from server.models.models import Product
from sqlalchemy.exc import SQLAlchemyError
from server.schemas import product_schemas

router = APIRouter(prefix="/product", tags=["Product  CRUD"])

@router.post("/create", status_code=status.HTTP_201_CREATED)

def create_product(product: product_schemas.ProductCreate = Body(...)):
    # Convert the Pydantic model to a SQLAlchemy model
    db_product = Product(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product