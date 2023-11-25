from sqlalchemy import  Column, Integer, String, ForeignKey,Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from server.db.db import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    billing_address = Column(String,nullable=True)
    shipping_address = Column(String,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    
    # Establishing relationships
    reviews = relationship("Review", back_populates="user")
    # purchased_products = relationship("Product", secondary="user_purchase", back_populates="buyers")
    cart_items = relationship("Cart", back_populates="user")
    favorite_items = relationship("Favorite", back_populates="user")
    purchases = relationship("UserPurchase", back_populates="user")  # Added this line
        
    

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    parent_category_id = Column(Integer, ForeignKey('product_categories.id',ondelete="SET NULL"))
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
    product_size = Column(String)
    SKU = Column(String)
    target_audience = Column(String)
    product_color = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    category_id = Column(Integer, ForeignKey('product_categories.id',ondelete="SET NULL"))
    
    # Establishing relationships
    category = relationship("ProductCategory", back_populates="products")
    # buyers = relationship("User", secondary="user_purchase", back_populates="purchased_products")
    reviews = relationship("Review", back_populates="product")  # Added this line

    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    carts = relationship("Cart", back_populates="product", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")
    purchases = relationship("UserPurchase", back_populates="product")  # Added this line


class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    discount_percent = Column(Float)
    sale_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
 
    # Establishing many-to-many relationship with Product
    products = relationship("Product", secondary="product_sales", back_populates="sales")

class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    image_path = Column(String)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="SET NULL"), nullable=True)    
    # Establishing relationship with Product
    product = relationship("Product", back_populates="images") 



class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id',ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey('users.id',ondelete="SET NULL"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # Establishing relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))  # Updated here
    product_id = Column(Integer, ForeignKey('products.id', ondelete="SET NULL")) 
    quantity = Column(Integer, default=1)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Establishing relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="carts")


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))  # Updated here
    product_id = Column(Integer, ForeignKey('products.id', ondelete="SET NULL"))  
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Establishing relationships
    user = relationship("User", back_populates="favorite_items")
    product = relationship("Product", back_populates="favorites")

 
class UserPurchase(Base):
    __tablename__ = 'user_purchases'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    product_id = Column(Integer, ForeignKey('products.id', ondelete="SET NULL"))
    status = Column(String, default='pending') # Add your desired data type
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Establishing relationships
    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="buyers")


# Association table for the many-to-many relationship between User and Product
# user_purchase_association = Table('user_purchase', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id',ondelete="SET NULL")),
#     Column('product_id', Integer, ForeignKey('products.id',ondelete="SET NULL"))
# )


# Association Table for Product and Sales (many-to-many relationship)
product_sales_association = Table(
    'product_sales',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('sales_id', Integer, ForeignKey('sales.id')),
)

# Connecting the many-to-many relationship
Product.sales = relationship("Sales", secondary=product_sales_association, back_populates="products")
