from random import uniform

from sqlalchemy import text
from sqlalchemy.orm import Session
from src.db.db_init import get_db, engine
from src.db.models import Base, CategoryDb, ProductDb, ProductSellerDb, RolesDb, RolesValues, SellerDb, UserDb

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

products = [
    {
        "id": 1,
        "title": 'FVP 495K6 Multi-V',
        "description": 'some desc',
        "thumbnail": 'http://some-domain.com/multi-v.png',
        "category_id": 2
    },
    {
        "id": 2,
        "title": 'DAYCO 5060495DR Drive Rite',
        "description": 'some desc',
        "thumbnail": 'http://some-domain.com/mileage_maker_multi_v_belt.png',
        "category_id": 2
    },
    {
        "id": 3,
        "title": 'BANDO 6PK1255',
        "description": 'some desc',
        "thumbnail": 'https://some-domain.com/various-mfr-T01218148.png',
        "category_id": 2
    },
    {
        "id": 4,
        "title": 'CONTINENTAL 6PK1256',
        "description": 'some desc',
        "thumbnail": 'https://some-domain.com/various-mfr-T01218148.png',
        "category_id": 2
    },
    {
        "id": 5,
        "title": 'SKP SK39106',
        "description": 'some desc',
        "thumbnail": 'https://some-domain.com/various-mfr-T01218148.png',
        "category_id": 3,
    },
    {
        "id": 6,
        "title": 'ULTRA-POWER 39106',
        "description": 'some desc',
        "thumbnail": 'https://some-domain.com/various-mfr-T01218148.png',
        "category_id": 3,
    },
]

sellers = [
    {
        "id": 1,
        "seller_name": "Ibn Haidra"
    },
    {
        "id": 2,
        "seller_name": "Al Nahdi"
    }
]

product_sellers = [
    {
        "product_id": 1,
        "seller_id": 1
    },
    {
        "product_id": 2,
        "seller_id": 1
    },
    {
        "product_id": 3,
        "seller_id": 1
    },
    {
        "product_id": 4,
        "seller_id": 1
    },
    {
        "product_id": 5,
        "seller_id": 1
    },
    {
        "product_id": 6,
        "seller_id": 1
    },
    {
        "product_id": 1,
        "seller_id": 2
    },
    {
        "product_id": 2,
        "seller_id": 2
    },
    {
        "product_id": 3,
        "seller_id": 2
    },
    {
        "product_id": 4,
        "seller_id": 2
    },
    {
        "product_id": 5,
        "seller_id": 2
    },
    {
        "product_id": 6,
        "seller_id": 2
    },
]

product_category = [
    {
        "category": 2,
        "product": 1
    },
    {
        "category": 2,
        "product": 2,
    },
    {
        "category": 2,
        "product": 3
    },
    {
        "category": 2,
        "product": 4
    },
    {
        "category": 3,
        "product": 5
    },
    {
        "category": 3,
        "product": 6
    }
]

categories = [
    {

        "id": 1,
        "name": "Belt Drive",
        "parent_id": None,
        "children": [
            {
                "id": 2,
                "name": "Belt",
                "parent_id": 1,
            },
            {
                "id": 3,
                "name": "Belt Tensioner",
                "parent_id":  1
            },
            {
                "id": 4,
                "name": "Tensioner Pulley",
                "parent_id":  1
            },
        ]
    },
    {
        "id": 5,
        "name": "Body & Lamp Assembly",
        "parent_id": None,
        "children": [
            {
                "id": 6,
                "name": "Toggle	Air Deflector",
                "parent_id": 5,
            },
            {
                "id": 7,
                "name": "Toggle	Bumper Bracket",
                "parent_id": 5,
            },
            {
                "id": 8,
                "name": "Bumper Cover",
                "parent_id": 5,
            }
        ]
    },
]

roles = [
    RolesValues.SELLER.value,
    RolesValues.ADMIN.value,
    RolesValues.CUSTOMER.value
]


def clear_db():
    db: Session = next(get_db())

    db.execute(text("DROP SCHEMA public CASCADE"))
    db.execute(text("CREATE SCHEMA public"))

    db.commit()
    Base.metadata.create_all(bind=engine)


def add_categories():
    db: Session = next(get_db())

    for cat in categories:
        cat_obj = CategoryDb(
            id=cat["id"], name=cat["name"], parent_id=cat["parent_id"])
        db.add(cat_obj)
        for child_cat in cat["children"]:
            child_cat_obj = CategoryDb(
                id=child_cat["id"], name=child_cat["name"], parent_id=child_cat["parent_id"])
            db.add(child_cat_obj)

    db.commit()


def add_products():
    db: Session = next(get_db())

    # add products
    for prod in products:
        product_obj = ProductDb(
            id=prod['id'],
            title=prod['title'],
            description=prod['description'],
            thumbnail=prod['thumbnail'],
            category_id=prod['category_id'])

        db.add(product_obj)

    db.commit()


def add_sellers():
    db: Session = next(get_db())

    # add sellers
    for seller in sellers:
        seller_obj = SellerDb(seller_name=seller["seller_name"])
        db.add(seller_obj)

    db.commit()


def add_product_sellers():
    db: Session = next(get_db())

    # add product sellers and their prices
    for product_seller in product_sellers:
        prod_seller_obj = ProductSellerDb(
            product_id=product_seller["product_id"], seller_id=product_seller["seller_id"],
            price=uniform(10, 100))
        db.add(prod_seller_obj)

    db.commit()


def add_roles():
    db: Session = next(get_db())
    
    for role in roles:
        created_role = RolesDb(role=role)
        db.add(created_role)

    db.commit()


def add_test_user():
    db: Session = next(get_db())
    user = UserDb()
    user.email = "test@test.com"    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user.hashed_password = pwd_context.hash("123456")
    
    user.user_role = RolesValues.CUSTOMER.value
    
    db.add(user)
    
    db.commit()

def main():
    clear_db()

    add_categories()

    add_products()

    add_sellers()

    add_product_sellers()
    
    add_roles()
    
    add_test_user()


if __name__ == "__main__":
    main()
