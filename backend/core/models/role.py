from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

# Таблица связи многие-ко-многим: пользователи → роли
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

# Таблица связи многие-ко-многим: роли → разрешения
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  # owner, developer, supervisor, manager, support, customer, executor
    description = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    
    def __repr__(self):
        return f"<Role(name={self.name})>"

class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)  # create_order, edit_order, view_users, etc.
    resource = Column(String(50))  # orders, users, disputes, etc.
    action = Column(String(20))    # create, read, update, delete, manage
    description = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission(name={self.name})>"
