from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.routers import auth, categories, products

app = FastAPI(
    title="Product Catalog API",
    description="A CRUD REST API for managing products and categories",
    version="1.0.0",
    docs_url=None,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Product Catalog API - Docs",
        swagger_favicon_url="/static/favicon.ico",
    )


@app.get("/")
def root():
    return {"message": "Product Catalog API is running"}
