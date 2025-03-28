from sqlalchemy import Column, ForeignKey, Table
from models.base import Base

product_tag = Table(
    "product_tag",
    Base.metadata,
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)    
