from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_serializer import SerializerMixin
from db.db_init import engine

metadata = MetaData()


class Base(DeclarativeBase, SerializerMixin):
    pass


Base.metadata.create_all(bind=engine)

