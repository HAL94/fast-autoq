from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

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