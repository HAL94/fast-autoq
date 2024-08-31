from db.base import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric

class SellerDb(Base):
    __tablename__ = 'sellers'

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_name: Mapped[str] = mapped_column()
    products: Mapped["ProductSellerDb"] = relationship(back_populates="seller")

    def __repr__(self) -> str:
        return f"<Seller({self.seller_name})>"

class ProductSellerDb(Base):
    __tablename__ = "product_sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    product: Mapped["ProductDb"] = relationship(back_populates="sellers") # type: ignore
    seller: Mapped["SellerDb"] = relationship(back_populates="products")

    def __repr__(self) -> str:
        return f"ProductSeller<{self.seller}, {self.id}>"