from fastapi import FastAPI, Request
from server.utils.rate_limit import rate_limited
from fastapi.middleware.cors import CORSMiddleware
from server.routers import (
    sales_router,
    user_router, 
    product_catogory_router, 
    product_router, 
    reviews_routers, 
    filter_products_router, 
    cart_router,
    favorites_router,
    user_paches_router,
    landing_page_router,
    featured_product_router,
    product_image_router,
    auth_router,
    reset_password_router,
    banners_router,
)

app = FastAPI(title="Shopping center App Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# router for admin auth routes
app.include_router(product_catogory_router.router)
app.include_router(product_router.router)
app.include_router(product_image_router.router)
app.include_router(featured_product_router.router)
app.include_router(sales_router.router)
app.include_router(banners_router.router)


# router for user auth routes
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(reset_password_router.router)
app.include_router(reviews_routers.router)
app.include_router(cart_router.router)
app.include_router(favorites_router.router)
app.include_router(user_paches_router.router)



# neutral routes
app.include_router(filter_products_router.router)
app.include_router(landing_page_router.router)

# app.include_router(user_prompt_router.router)

@app.get("/ping")
@rate_limited(max_calls=10, time_frame=60)
async def health_check(request:Request):
    """Health check."""

    return {"message": "Hello I am working!"}

@app.get("/")
@rate_limited(max_calls=10, time_frame=60)
async def intro(request: Request):
    """
    This Endpoint for intro to this backend
    """
    return {"message": "Welcome to the shopping Backend"}