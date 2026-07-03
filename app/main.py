from fastapi import FastAPI
from app.routers import auth, categories, products

app = FastAPI(
    title="Product Catalog API",
    description="A CRUD REST API for managing products and categories",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "Product Catalog API is running"}
