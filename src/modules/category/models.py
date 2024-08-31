from typing import List
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class CategoryDb(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

    children: Mapped[List["CategoryDb"]] = relationship()

    products: Mapped[List["ProductDb"]] = relationship( # type: ignore
        back_populates="category")

    def __repr__(self) -> str:
        return f"Category<{self.name}>"