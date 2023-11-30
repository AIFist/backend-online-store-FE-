from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers import (
    user_router, 
    product_catogory_router, 
    product_router, 
    reviews_routers, 
    filter_products_router, 
    cart_router,
    favorites_router
)

app = FastAPI(title="Shopping center App Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
 
app.include_router(user_router.router)
app.include_router(product_catogory_router.router)
app.include_router(product_router.router)
app.include_router(filter_products_router.router)
app.include_router(reviews_routers.router)
app.include_router(cart_router.router)
app.include_router(favorites_router.router)

# app.include_router(user_prompt_router.router)

@app.get("/ping")
def health_check():
    """Health check."""

    return {"message": "Hello I am working!"}

@app.get("/")
def intro():
    """
    This Endpoint for intro to this backend
    """
    return {"message": "Welcome to the shopping Backend"}