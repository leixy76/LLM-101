"""
SQLAlchemy ORM models for the AI Travel Planner system.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import (
    String, Text, Integer, Float, Boolean, DateTime, Date, 
    ForeignKey, JSON, Enum as SQLEnum, DECIMAL, Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .config import Base
from ..models.base import TravelStyle, PlanStatus, ConversationStatus, MessageRole, Currency


class UserORM(Base):
    """User ORM model."""
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic info
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Preferences (stored as JSON)
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    travel_history: Mapped[list] = mapped_column(JSON, default=list)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    travel_plans: Mapped[List["TravelPlanORM"]] = relationship(
        "TravelPlanORM", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    conversations: Mapped[List["ConversationORM"]] = relationship(
        "ConversationORM", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class TravelPlanORM(Base):
    """Travel Plan ORM model."""
    
    __tablename__ = "travel_plans"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    destination: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    destinations: Mapped[list] = mapped_column(JSON, default=list)
    
    # Dates
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Budget
    budget: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(SQLEnum(Currency), default=Currency.USD)
    estimated_total_cost: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2))
    
    # Status and details
    status: Mapped[PlanStatus] = mapped_column(SQLEnum(PlanStatus), default=PlanStatus.PLANNING)
    travelers_count: Mapped[int] = mapped_column(Integer, default=1)
    travel_style: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # JSON fields for complex data
    flights: Mapped[list] = mapped_column(JSON, default=list)
    hotels: Mapped[list] = mapped_column(JSON, default=list)
    itinerary: Mapped[list] = mapped_column(JSON, default=list)
    special_requirements: Mapped[list] = mapped_column(JSON, default=list)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="travel_plans")
    
    # Indexes
    __table_args__ = (
        Index('ix_travel_plans_user_status', 'user_id', 'status'),
        Index('ix_travel_plans_dates', 'start_date', 'end_date'),
    )
    
    def __repr__(self) -> str:
        return f"<TravelPlan(id={self.id}, title={self.title}, destination={self.destination})>"


class ConversationORM(Base):
    """Conversation ORM model."""
    
    __tablename__ = "conversations"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Basic info
    title: Mapped[Optional[str]] = mapped_column(String(200))
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus), 
        default=ConversationStatus.ACTIVE
    )
    
    # Context and metadata
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="conversations")
    messages: Mapped[List["MessageORM"]] = relationship(
        "MessageORM", 
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageORM.timestamp"
    )
    
    # Indexes
    __table_args__ = (
        Index('ix_conversations_user_status', 'user_id', 'status'),
        Index('ix_conversations_updated', 'updated_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, user_id={self.user_id}, status={self.status})>"


class MessageORM(Base):
    """Message ORM model."""
    
    __tablename__ = "messages"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key
    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("conversations.id"), 
        nullable=False
    )
    
    # Message content
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # AI model info
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    model_name: Mapped[Optional[str]] = mapped_column(String(100))
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    conversation: Mapped["ConversationORM"] = relationship("ConversationORM", back_populates="messages")
    
    # Indexes
    __table_args__ = (
        Index('ix_messages_conversation_timestamp', 'conversation_id', 'timestamp'),
        Index('ix_messages_role', 'role'),
    )
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"