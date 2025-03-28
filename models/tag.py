import uuid
from models.base import Base
from models.product_tag import product_tag
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid



class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    products = relationship("Product", secondary=product_tag, back_populates="tags")
