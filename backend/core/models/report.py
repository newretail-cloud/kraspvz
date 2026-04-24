from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.sql import func
from core.database import Base

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, nullable=False)
#    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    
    # Тип отчёта: start, end
    report_type = Column(String(10), nullable=False)
    
    # Фото (храним URL или пути)
    photo_pvz = Column(String(500))
    photo_storage = Column(String(500))
    photo_computer = Column(String(500))
    photo_goods = Column(String(500))  # начальные товары
    photo_clean = Column(String(500))   # уборка
    photo_returns = Column(String(500)) # возвраты
    photo_boxes = Column(String(500))   # подготовленные коробки
    
    # Комментарий
    comment = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<Report(shift={self.shift_id}, type={self.report_type})>"
