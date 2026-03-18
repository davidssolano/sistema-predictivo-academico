from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Lee la URL de tu base de datos desde la variable de entorno de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Si por alguna razón falla, usamos sqlite local como respaldo temporal
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para que main.py pueda pedir una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()