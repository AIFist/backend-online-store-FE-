from sqlalchemy import  Column, Integer, String, ForeignKey,Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from server.db.db import Base, engine, db
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    
    # Establishing relationships
    reviews = relationship("Review", back_populates="user")
    purchased_products = relationship("Product", secondary="user_purchase", back_populates="buyers")

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    parent_category_id = Column(Integer, ForeignKey('product_categories.id'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    # Establishing a relationship with itself (self-referencing)
    parent_category = relationship("ProductCategory", remote_side=[id])
    subcategories = relationship("ProductCategory", back_populates="parent_category")

    # Corrected relationship with Product
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Integer)
    stock_quantity = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    category_id = Column(Integer, ForeignKey('product_categories.id'))
    
    # Establishing relationships
    category = relationship("ProductCategory", back_populates="products")
    buyers = relationship("User", secondary="user_purchase", back_populates="purchased_products")
    reviews = relationship("Review", back_populates="product")  # Added this line

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # Establishing relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

# Association table for the many-to-many relationship between User and Product
user_purchase_association = Table('user_purchase', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


Base.metadata.create_all(engine)


session = db

if __name__ == "__main__":
    from datetime import datetime

    # Assuming you have already created the tables and the session
    # session = db

    # Adding a user
    user1 = User(username='JohnDoe', email='john@example.com', password='password123')
    session.add(user1)

    # Adding a product category
    electronics = ProductCategory(category_name='Electronics')
    session.add(electronics)

    # Adding a product
    laptop_product = Product(
        product_name='Laptop',
        description='Powerful laptop',
        price=999,
        stock_quantity=10,
        category=electronics
    )
    session.add(laptop_product)

    # Adding a review
    review = Review(
        product=laptop_product,
        user=user1,
        rating=5,
        comment='Great product!'
    )
    session.add(review)

    # Committing the changes to the database
    session.commit()
