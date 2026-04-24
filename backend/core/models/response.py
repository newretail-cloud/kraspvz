from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from core.database import Base

class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    executor_id = Column(Integer, nullable=False)
#    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
#    executor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Статус: pending, accepted, rejected, cancelled
    status = Column(String(20), default='pending')
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Response(order={self.order_id}, executor={self.executor_id}, status={self.status})>"
