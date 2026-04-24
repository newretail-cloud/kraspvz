from sqlalchemy.orm import Session
from typing import Optional, List
from core.models import User, Role
from core.security.auth import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, telegram_id: Optional[int] = None, max_user_id: Optional[str] = None,
                    phone: str = None, full_name: str = None, 
                    role_name: str = "executor", password: str = None) -> User:
        """Создание нового пользователя"""
        # Получаем роль
        role = self.db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"Роль {role_name}")
            self.db.add(role)
            self.db.flush()
        
        user = User(
            telegram_id=telegram_id,
            max_user_id=max_user_id,
            phone=phone,
            full_name=full_name,
            role=role_name,  # временное поле
            hashed_password=get_password_hash(password) if password else None
        )
        user.roles.append(role)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_telegram(self, telegram_id: int) -> Optional[User]:
        """Поиск пользователя по Telegram ID"""
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()
    
    def get_user_by_max(self, max_user_id: str) -> Optional[User]:
        """Поиск пользователя по MAX ID"""
        return self.db.query(User).filter(User.max_user_id == max_user_id).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Поиск пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Обновление данных пользователя"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate(self, telegram_id: Optional[int] = None, 
                     max_user_id: Optional[str] = None,
                     password: str = None) -> Optional[User]:
        """Аутентификация пользователя"""
        user = None
        if telegram_id:
            user = self.get_user_by_telegram(telegram_id)
        elif max_user_id:
            user = self.get_user_by_max(max_user_id)
        
        if not user:
            return None
        
        if password and not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def assign_role(self, user_id: int, role_name: str) -> bool:
        """Назначение роли пользователю"""
        user = self.get_user_by_id(user_id)
        role = self.db.query(Role).filter(Role.name == role_name).first()
        
        if not user or not role:
            return False
        
        if role not in user.roles:
            user.roles.append(role)
            self.db.commit()
        return True
    
    def has_permission(self, user_id: int, permission_name: str) -> bool:
        """Проверка наличия права у пользователя"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        for role in user.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False
