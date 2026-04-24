from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.sql import func
from core.database import Base

class Shift(Base):
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    executor_id = Column(Integer, nullable=False)
#    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
#    executor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    
    # Статус: assigned, started, completed, disputed
    status = Column(String(20), default='assigned')
    
    # Отметки о начале/конце
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<Shift(order={self.order_id}, executor={self.executor_id}, status={self.status})>"
