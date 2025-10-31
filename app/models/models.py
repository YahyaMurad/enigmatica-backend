import datetime

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    machines = relationship(
        "Machine", back_populates="user", cascade="all, delete-orphan"
    )
    heartbeats = relationship(
        "Heartbeat", back_populates="user", cascade="all, delete-orphan"
    )
    daily_activities = relationship(
        "DailyActivity", back_populates="user", cascade="all, delete-orphan"
    )
    api_keys = relationship(
        "APIKey", back_populates="user", cascade="all, delete-orphan"
    )


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC).date())
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_name = Column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="machines")
    heartbeats = relationship(
        "Heartbeat", back_populates="machine", cascade="all, delete-orphan"
    )


class Heartbeat(Base):
    __tablename__ = "heartbeats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)

    entity = Column(String, nullable=False)
    type = Column(String)
    category = Column(String)
    time = Column(TIMESTAMP, nullable=False)
    project = Column(String)
    branch = Column(String)
    language = Column(String)
    lines = Column(Integer)
    lineno = Column(Integer)
    cursorpos = Column(Integer)
    is_write = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="heartbeats")
    machine = relationship("Machine", back_populates="heartbeats")


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    total_active_seconds = Column(Integer, default=0)
    project_worked_on = Column(JSON, default={})

    # Relationship
    user = relationship("User", back_populates="daily_activities")
