#файл models служит для описание структуры базы данных

from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey # Импортируем необходимые классы и функции из SQLAlchemy, следующие классы: Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship # Импортируем класс relationship для создания связей между таблицами
from database import Base # Импортируем базовый класс Base из файла database.py

# Таблица customers
class Customer(Base):
    __tablename__ = "customers"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FirstName = Column(String(30), nullable=False) # Бывшее название FirstName
    LastName = Column(String(25), nullable=False)  # Новое поле

    # Связь с таблицей orders (один-ко-многим)
    orders = relationship("Order", back_populates="customer")

# Таблица products
class Product(Base):
    __tablename__ = "products"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ProductName = Column(String(30), nullable=False)
    Manufacturer = Column(String(20), nullable=False)
    ProductCount = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 0), nullable=False)

    # Связь с таблицей orders (один-ко-многим)
    orders = relationship("Order", back_populates="product")

# Таблица orders
class Order(Base):
    __tablename__ = "orders"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ProductId = Column(Integer, ForeignKey("products.Id"), nullable=False)
    CustomerId = Column(Integer, ForeignKey("customers.Id"), nullable=False)
    CreatedAt = Column(Date, nullable=False)
    ProductCount = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 0), nullable=False)

    # Связи с таблицами customers и products
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")