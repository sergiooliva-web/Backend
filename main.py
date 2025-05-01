# Основной файл приложения FastAPI для работы с базой данных SQLite и таблицами Customers, Products и Orders
# Импортируем необходимые библиотеки и модули для работы с FastAPI и SQLAlchemy
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates # Импортируем Jinja2Templates для работы с шаблонами
from fastapi.responses import FileResponse # Импортируем FileResponse для работы с файлами
import logging # Импортируем модуль для логирования отладочных сообщений
from datetime import date

from models import Order, Product # Импортируем модели Order и Product из файла models.py

logging.basicConfig(level=logging.INFO) # Настраиваем уровень логирования
logger = logging.getLogger(__name__) # Создаем логгер для отладки

from models import Base
from crud import ( # Импортируем функции для работы с базой данных из файла crud.py
    get_customers, create_customer,
    get_products, create_product,
    get_orders, create_order
)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

class CustomerCreate(BaseModel): # Создаем класс для таблицы Customer
    Id: int
    FirstName: str
    LastName: str

    class Config:
        from_attributes = True  # Указываем, что модель будет работать с ORM (Object Relational Mapping)    

class ProductCreate(BaseModel): # Cоздаем класс для таблицы Product
    Id: int
    ProductName: str
    Manufacturer: str
    ProductCount: int
    Price: float    

class Product(ProductCreate):
    Id: int  # Для чтения клиента Id обязателен

    class Config:
        from_attributes = True   # Указываем, что модель будет работать с ORM (Object Relational Mapping)        

class OrderCreate(BaseModel): # Создаем класс для таблицы Order
    ProductId: int
    CustomerId: int
    CreatedAt: date  # Формат YYYY-MM-DD
    ProductCount: int
    Price: float

class Order(OrderCreate):
    Id: int  # Для чтения клиента Id обязателен

    class Config:
        from_attributes = True   # Указываем, что модель будет работать с ORM (Object Relational Mapping)     

def get_db(): # Создаем зависимость для работы с базой данных
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI() # Создаем экземпляр FastAPI

templates = Jinja2Templates(directory="templates")  # Указываем директорию для шаблонов

@app.get("/") # Главная страница приложения
def read_root():
    return FileResponse("static/index.html") 

@app.get("/customers", response_model=list[CustomerCreate])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching customers with skip={skip}, limit={limit}")
    return get_customers(db, skip=skip, limit=limit)


@app.post("/customers", response_model=CustomerCreate)
def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, first_name=customer.FirstName, last_name=customer.LastName)



# Маршруты для таблицы products
@app.get("/products", response_model=list[ProductCreate])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching products with skip={skip}, limit={limit}")
    return get_products(db, skip=skip, limit=limit)

@app.post("/products", response_model=ProductCreate)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data=product.dict())

# Маршруты для таблицы orders
@app.get("/orders", response_model=list[OrderCreate])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching orders with skip={skip}, limit={limit}")
    return get_orders(db, skip=skip, limit=limit)

@app.post("/orders", response_model=OrderCreate)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order_data=order.dict())