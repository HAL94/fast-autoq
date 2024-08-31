from db.base import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class ProductDb(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True)
    
    category: Mapped["CategoryDb"] = relationship(back_populates="products") # type: ignore

    sellers: Mapped[List["ProductSellerDb"] # type: ignore
                    ] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"Product<{self.id}, {self.title}>"