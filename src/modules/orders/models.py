import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from modules.sellers.models import SellerDb

class OrderDb(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column()
    fulfillment_status: Mapped[str] = mapped_column()
    payment_status: Mapped[str] = mapped_column()

    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    cart: Mapped["CartDb"] = relationship() # type: ignore

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    customer: Mapped["UserDb"] = relationship() # type: ignore

    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    currency_code: Mapped[str] = mapped_column()
    tax_rate: Mapped[float] = mapped_column()

    canceld_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))
    seller: Mapped["SellerDb"] = relationship() # type: ignore

    order_amount: Mapped[float] = mapped_column()