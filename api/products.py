from database.database import Database
from fastapi import APIRouter, Depends, status
from schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession


products_router = APIRouter(
    tags=["products"],
    
)


@products_router.get("/products", status_code=status.HTTP_200_OK)
async def list_products(
    tag: str = None, 
    in_stock: bool = False, 
    session: AsyncSession = Depends(Database().get_session)
):
    products = await ProductService(session).list_products(tag_filter=tag, in_stock_filter=in_stock)
    return [ProductResponse(**product.serialize()) for product in products]  # convert SQLAlchemy models to Pydantic models

@products_router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(
    product: ProductCreateRequest, 
    session: AsyncSession = Depends(Database().get_session)):
    product = await ProductService(session).create_product(product)
    return ProductResponse(**product.serialize())

@products_router.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_product(
    product_id: str, 
    session: AsyncSession = Depends(Database().get_session)):
    product = await ProductService(session).get_product(product_id)
    return ProductResponse(**product.serialize())

@products_router.put("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product(
    product_id: str, 
    product_update: ProductUpdateRequest, 
    session: AsyncSession = Depends(Database().get_session)):
    product = await ProductService(session).update_product(product_id, product_update)
    return ProductResponse(**product.serialize())

@products_router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str, 
    session: AsyncSession = Depends(Database().get_session)):
    await ProductService(session).delete_product(product_id)
    return {"message": "Product deleted successfully"}

