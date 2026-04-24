from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2.extras

DATABASE_URL = "postgresql://pvz_user:pvz_password123@localhost:5432/pvz_bot"

# Добавляем параметры для совместимости типов
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        'options': '-c timezone=utc'
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Создаёт все таблицы в базе данных"""
    from core.models import (
        User, Order, Response, Shift, Report,
        Role, Permission, user_roles, role_permissions
    )
    Base.metadata.create_all(bind=engine)
