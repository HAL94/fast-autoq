import enum
from typing import List
from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

class CartStatusValues(enum.Enum):
    ACTIVE = 'ACTIVE'
    ORDER_COMPLETED = 'ORDER_COMPLETED'


CartStatusEnum = Enum(CartStatusValues.ACTIVE.value,
                      CartStatusValues.ORDER_COMPLETED.value, name='cart-status')


class LineTypeValues(enum.Enum):
    ORDER = 'ORDER'
    CART = 'CART'
    

LineTypeEnum = Enum(LineTypeValues.CART.value, LineTypeValues.ORDER.value, name='line-type')


class CartDb(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)

    # customer
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDb"] = relationship(back_populates="user_cart") # type: ignore

    cart_items: Mapped[List["LineItemDb"]] = relationship(back_populates="cart", primaryjoin=f"and_(CartDb.id==LineItemDb.cart_id, LineItemDb.line_type=='{LineTypeValues.CART.value}')")

    status: Mapped[Enum] = mapped_column(CartStatusEnum, nullable=True)
    total: Mapped[float] = mapped_column(default=0)
    # cascade="all,delete", backref="parent"


class LineItemDb(Base):
    __tablename__ = "line_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", "seller_id",
                         name="unique_product_seller_in_user_cart"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # cart
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("cart.id"), nullable=True)
    cart: Mapped["CartDb"] = relationship(back_populates="cart_items")

    # product
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["ProductDb"] = relationship() # type: ignore

    # seller
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))
    seller: Mapped["SellerDb"] = relationship() # type: ignore
    
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=True)
    # order = relationship("OrderDb", backref="OrderDb.id")
    order: Mapped["OrderDb"] = relationship() # type: ignore
    

    purchase_price: Mapped[float] = mapped_column()
    qty: Mapped[int] = mapped_column()
    total: Mapped[float] = mapped_column()
    
    line_type: Mapped[Enum] = mapped_column(LineTypeEnum, nullable=False)