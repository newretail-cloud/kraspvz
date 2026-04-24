from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from core.models import User, Order, Response

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, customer_id: int, marketplace: str, address: str,
                    work_date: datetime, cells_count: int, price_min: int,
                    price_max: Optional[int] = None, taxi_paid: bool = False,
                    payment_method: str = "card", key_info: str = None,
                    contact_phone: str = None, extra_info: str = None) -> Order:
        """Создание нового заказа (объявления)"""
        
        # Проверяем существование пользователя
        customer = self.db.query(User).filter(User.id == customer_id).first()
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")
        
        order = Order(
            customer_id=customer_id,
            marketplace=marketplace,
            address=address,
            work_date=work_date,
            cells_count=cells_count,
            price_min=price_min,
            price_max=price_max,
            taxi_paid=taxi_paid,
            payment_method=payment_method,
            key_info=key_info,
            contact_phone=contact_phone,
            extra_info=extra_info,
            status='active'
        )
        
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_orders(self, status: Optional[str] = 'active', skip: int = 0, limit: int = 100) -> List[Order]:
        """Получение списка заказов с фильтрацией по статусу"""
        query = self.db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.offset(skip).limit(limit).all()
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Получение заказа по ID"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        """Получение заказов заказчика"""
        return self.db.query(Order).filter(Order.customer_id == customer_id).all()
    
    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        """Обновление статуса заказа"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete_order(self, order_id: int) -> bool:
        """Удаление заказа (только в статусе draft или active)"""
        order = self.get_order_by_id(order_id)
        if not order or order.status not in ['draft', 'active']:
            return False
        self.db.delete(order)
        self.db.commit()
        return True
