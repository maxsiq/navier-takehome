import uuid
from models.base import Base
from models.product_tag import product_tag
from sqlalchemy import CheckConstraint 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional


class Product(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column()
    price: Mapped[float] = mapped_column(nullable=False)
    in_stock: Mapped[bool] = mapped_column(default=True)

    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=product_tag, lazy="selectin", back_populates="products")

    # field constraints
    __table_args__ = (
        CheckConstraint("price > 0", name="price_is_positive"),
    )

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "in_stock": self.in_stock,
            "tags": [tag.name for tag in self.tags] if self.tags else []
        }
