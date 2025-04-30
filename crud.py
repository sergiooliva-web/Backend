from sqlalchemy.orm import Session
from models import Customer, Product, Order

# Функция принимает три параметра: db: Session - объект сессии базы данных (создается через SessionLocal в SQLAlchemy) skip: int = 0, limit: int = 10 (max - 10 количество записей)
# db.query(Customer) создает запрос к таблице customers в базе данных,
# Метод .offset(skip) пропускает первые skip записей
# Метод .limit(limit) ограничивает количество возвращаемых записей до limit
def get_customers(db: Session, skip: int = 0, limit: int = 10): 
    return db.query(Customer).offset(skip).limit(limit).all() 

def create_customer(db: Session, first_name: str, last_name: str): # Функция для создания нового клиента
    db_customer = Customer(FirstName=first_name, LastName=last_name)
    db.add(db_customer) # Добавление обьектов в сессию
    db.commit() # Фиксируем изменения в базе данных
    db.refresh(db_customer)  # Обновляем объект после сохранения
    return db_customer  # Возвращаем созданный объект

# CRUD для таблицы products
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_data):
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# CRUD для таблицы orders
def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def create_order(db: Session, order_data):
    db_order = Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order