from turtle import back
from typing import List
from sqlalchemy import Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, MetaData, Numeric, UniqueConstraint
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, DeclarativeBase
import enum
from .db_init import engine

from sqlalchemy_serializer import SerializerMixin


# BaseDb = declarative_base()

class Base(DeclarativeBase, SerializerMixin):
    pass


metadata = MetaData()


class RolesValues(enum.Enum):
    SELLER = "SELLER"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


RolesEnum = Enum(RolesValues.SELLER.value,
                 RolesValues.CUSTOMER.value,
                 RolesValues.ADMIN.value, name='role')

# product_sellers = Table(
#     "product_sellers",
#     Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column("product", ForeignKey("products.id")),
#     Column("seller", ForeignKey("sellers.id")),
#     Column("price", Numeric(10, 2))
# )


class RolesDb(Base):
    __tablename__ = "roles"
    role: Mapped[Enum] = Column(RolesEnum, unique=True, primary_key=True)
    user: Mapped[List["UserDb"]] = relationship()


class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    user_role: Mapped[str] = mapped_column(ForeignKey("roles.role"))
    user_cart: Mapped["CartDb"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User({self.email}, {self.id})>"


class VehicleMakeDb(Base):
    __tablename__ = "vehicle_makes"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(unique=True, index=True)
    models: Mapped[List["VehicleModelDb"]] = relationship()


class VehicleModelDb(Base):
    __tablename__ = "vehicle_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(unique=True, index=True)
    min_year: Mapped[int] = mapped_column()
    max_year: Mapped[int] = mapped_column()
    make_id: Mapped[int] = mapped_column(ForeignKey("vehicle_makes.id"))
    body_style: Mapped[str] = mapped_column()  # SUV, Sedan, etc..


class VehicleDb(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    make_id: Mapped[int] = mapped_column(ForeignKey("vehicle_makes.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("vehicle_models.id"))
    year: Mapped[int] = mapped_column()
    variants: Mapped[List["VehicleVariantDb"]] = relationship()


class VehicleVariantDb(Base):
    __tablename__ = "vehicle_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    engine_type: Mapped[str] = mapped_column()
    trim_level: Mapped[str] = mapped_column()
    transmission_type: Mapped[str] = mapped_column()
    drive_terain: Mapped[str] = mapped_column()


class SellerDb(Base):
    __tablename__ = 'sellers'

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_name: Mapped[str] = mapped_column()
    products: Mapped["ProductSellerDb"] = relationship(back_populates="seller")

    def __repr__(self) -> str:
        return f"<Seller({self.seller_name})>"


class CategoryDb(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

    children: Mapped[List["CategoryDb"]] = relationship()

    products: Mapped[List["ProductDb"]] = relationship(
        back_populates="category")

    def __repr__(self) -> str:
        return f"Category<{self.name}>"


class ProductDb(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True)
    category: Mapped["CategoryDb"] = relationship(back_populates="products")

    sellers: Mapped[List["ProductSellerDb"]
                    ] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"Product<{self.id}, {self.title}>"


class ProductSellerDb(Base):
    __tablename__ = "product_sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    product: Mapped["ProductDb"] = relationship(back_populates="sellers")
    seller: Mapped["SellerDb"] = relationship(back_populates="products")

    def __repr__(self) -> str:
        return f"ProductSeller<{self.seller}, {self.id}>"


class CartDb(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)

    # customer
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDb"] = relationship(back_populates="user_cart")

    cart_items: Mapped[List["CartItemDb"]] = relationship(
        back_populates="cart", cascade="all, delete")
    # cascade="all,delete", backref="parent"


class CartItemDb(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", "seller_id",
                         name="unique_product_seller_in_user_cart"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # cart
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("cart.id", ondelete='cascade'))
    cart: Mapped["CartDb"] = relationship(back_populates="cart_items")

    # product
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["ProductDb"] = relationship()

    # seller
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"))
    seller: Mapped["SellerDb"] = relationship()

    purchase_price: Mapped[float] = mapped_column()
    qty: Mapped[int] = mapped_column()


Base.metadata.create_all(bind=engine)
