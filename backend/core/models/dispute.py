from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Dispute(Base):
    __tablename__ = 'disputes'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    initiator_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # кто открыл спор
    respondent_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # с кем спор
    
    reason = Column(Text, nullable=False)  # причина спора
    description = Column(Text)
    
    status = Column(String(20), default='open')  # open, under_review, resolved_closed, resolved_refund
    resolution = Column(Text)  # решение модератора
    
    moderator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    resolved_at = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    order = relationship("Order", backref="disputes")
    initiator = relationship("User", foreign_keys=[initiator_id])
    respondent = relationship("User", foreign_keys=[respondent_id])
    moderator = relationship("User", foreign_keys=[moderator_id])
    
    def __repr__(self):
        return f"<Dispute(order={self.order_id}, status={self.status})>"

class Ticket(Base):
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    status = Column(String(20), default='open')  # open, in_progress, resolved, closed
    priority = Column(String(20), default='medium')  # low, medium, high, urgent
    
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    resolved_at = Column(DateTime)
    
    # Связи
    user = relationship("User", foreign_keys=[user_id])
    assignee = relationship("User", foreign_keys=[assigned_to])
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, user={self.user_id}, status={self.status})>"

class TicketMessage(Base):
    __tablename__ = 'ticket_messages'
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # внутренний комментарий для техподдержки
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    ticket = relationship("Ticket", backref="messages")
    author = relationship("User", foreign_keys=[author_id])
    
    def __repr__(self):
        return f"<TicketMessage(ticket={self.ticket_id}, author={self.author_id})>"
