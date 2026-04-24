from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan = Column(String(50), nullable=False)  # basic, pro, business
    price = Column(Float, nullable=False)
    
    posts_limit = Column(Integer, default=10)  # -1 для безлимита
    posts_used = Column(Integer, default=0)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    auto_renew = Column(Boolean, default=True)
    
    status = Column(String(20), default='active')  # active, expired, cancelled
    payment_id = Column(String(255))
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    user = relationship("User", backref="subscriptions")
    
    def __repr__(self):
        return f"<Subscription(user={self.user_id}, plan={self.plan}, status={self.status})>"

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    
    amount = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)  # subscription, post_fee, safe_deal, platform_fee, ad_placement
    description = Column(Text)
    
    payment_system_id = Column(String(255))  # ID в ЮKassa/Tinkoff
    status = Column(String(20), default='completed')  # pending, completed, failed, refunded
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    user = relationship("User", backref="transactions")
    order = relationship("Order", backref="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount})>"

class SafeDeal(Base):
    __tablename__ = 'safe_deals'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    executor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    amount = Column(Float, nullable=False)
    platform_fee = Column(Float, nullable=False)  # комиссия платформы
    executor_amount = Column(Float, nullable=False)  # сумма к выплате
    
    payment_id = Column(String(255))
    hold_id = Column(String(255))
    
    status = Column(String(20), default='pending')  # pending, held, released, refunded, disputed
    
    created_at = Column(DateTime, server_default=func.now())
    released_at = Column(DateTime)
    refunded_at = Column(DateTime)
    
    # Связи
    order = relationship("Order", backref="safe_deal")
    customer = relationship("User", foreign_keys=[customer_id])
    executor = relationship("User", foreign_keys=[executor_id])
    
    def __repr__(self):
        return f"<SafeDeal(order={self.order_id}, amount={self.amount}, status={self.status})>"

class PlatformEarning(Base):
    __tablename__ = 'platform_earnings'
    
    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)  # subscription, post_fee, ad, safe_deal
    source_id = Column(Integer)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<PlatformEarning(source={self.source}, amount={self.amount})>"
