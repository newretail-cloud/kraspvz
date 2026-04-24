from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True)
    max_user_id = Column(String(100), unique=True, nullable=True)
    role = Column(String(20), nullable=False)  # временно, для совместимости
    phone = Column(String(20))
    full_name = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Поля для исполнителя
    experience_months = Column(Integer, default=0)
    address = Column(String(300))
    lat = Column(Float)
    lon = Column(Float)
    max_cells = Column(Integer, default=0)
    
    # Системные поля
    is_blocked = Column(Boolean, default=False)
    blocked_until = Column(DateTime)
    rating = Column(Integer, default=0)
    
    # Связь с ролями (многие-ко-многим)
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.full_name})>"
    
    def has_permission(self, permission_name: str) -> bool:
        """Проверяет, есть ли у пользователя указанное разрешение"""
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False
    
    def has_role(self, role_name: str) -> bool:
        """Проверяет, есть ли у пользователя указанная роль"""
        return any(role.name == role_name for role in self.roles)
