from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.sql import func
from core.database import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)  # пока без ForeignKey
    
    # Информация о заказе
    marketplace = Column(String(20), nullable=False)  # WB, Ozon, Yandex
    address = Column(String(300), nullable=False)
    lat = Column(Float)  # широта
    lon = Column(Float)  # долгота
    work_date = Column(DateTime, nullable=False)
    duration_hours = Column(Integer, default=8)
    cells_count = Column(Integer, nullable=False)
    price_min = Column(Integer, nullable=False)
    price_max = Column(Integer)
    
    # Дополнительные опции
    taxi_paid = Column(Boolean, default=False)
    payment_method = Column(String(50))  # card, self_employed, cash
    
    # Контактная информация (раскрывается после подтверждения)
    key_info = Column(Text)
    contact_phone = Column(String(20))
    extra_info = Column(Text)
    
    # Фото ПВЗ (опционально)
    photo_url = Column(String(500))
    
    # Статус: active, in_progress, completed, cancelled
    status = Column(String(20), default='active')
    
    # Даты
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Order(id={self.id}, marketplace={self.marketplace}, price={self.price_min}-{self.price_max})>"
