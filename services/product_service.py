import uuid

from fastapi import HTTPException
from models import Product, Tag
from schemas.product import ProductCreateRequest, ProductUpdateRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_data: ProductCreateRequest) -> Product:
        # create a new product and associates tags
        tags = await self._get_or_create_tags(product_data.tags)

        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            in_stock=product_data.in_stock,
            tags=tags,
        )

        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def get_product(self, product_id: str) -> Product | None:
        try:
            uuid.UUID(product_id)  # validate UUID format
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product id")
        product = await self.session.get(Product, uuid.UUID(product_id))
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def list_products(
        self, tag_filter: str | None = None, in_stock_filter: bool = False
    ) -> list[Product]:
        query = select(Product)

        if tag_filter:
            query = query.join(Product.tags).where(Tag.name == tag_filter)

        if in_stock_filter:
            query = query.where(Product.in_stock.is_(True))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_product(
        self, product_id: str, product_update: ProductUpdateRequest
    ) -> Product:
        product = await self.get_product(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # update product attributes
        for key, value in product_update.model_dump().items():
            if key != "tags":
                setattr(product, key, value)

        # update tags
        tags = await self._get_or_create_tags(product_update.tags)
        product.tags = tags

        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product_id: str) -> None:
        product = await self.get_product(product_id)
        if product is None:  # no error if product not found
            return
        await self.session.delete(product)
        await self.session.commit()

    async def _get_or_create_tags(self, tag_names: list[str]) -> list[Tag]:
        tags = []
        for tag_name in tag_names:
            # check if the tag already exists, if not, create it
            query = select(Tag).where(Tag.name == tag_name)
            query_result = await self.session.execute(query)
            tag = query_result.scalars().one_or_none()
            if tag is None:
                tag = Tag(name=tag_name)
                self.session.add(tag)
                await self.session.commit()
                await self.session.refresh(tag)
            tags.append(tag)
        return tags
