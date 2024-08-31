import enum
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import Enum, Column
from db.base import Base

class RolesValues(enum.Enum):
    SELLER = "SELLER"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    
    

RolesEnum = Enum(RolesValues.SELLER.value,
                 RolesValues.CUSTOMER.value,
                 RolesValues.ADMIN.value, name='role')


class RolesDb(Base):
    __tablename__ = "roles"
    role: Mapped[Enum] = Column(RolesEnum, unique=True, primary_key=True)
    user: Mapped[List["UserDb"]] = relationship()


class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    user_role: Mapped[str] = mapped_column(ForeignKey("roles.role"))
    user_cart: Mapped["CartDb"] = relationship(back_populates="user") # type: ignore

    def __repr__(self) -> str:
        return f"<User({self.email}, {self.id})>"