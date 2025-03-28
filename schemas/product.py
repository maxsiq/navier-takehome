from pydantic import BaseModel, UUID4, Field
from typing import List, Optional


class TagResponse(BaseModel):
    name: str


class ProductSchema(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    price: float = Field(..., gt=0)
    in_stock: bool = Field(default=True)
    tags: Optional[List[str]] = Field()


class ProductCreateRequest(ProductSchema):
    pass  # All fields are required, inherited from ProductSchema


class ProductUpdateRequest(ProductSchema):
    pass


class ProductResponse(ProductSchema):
    id: UUID4
