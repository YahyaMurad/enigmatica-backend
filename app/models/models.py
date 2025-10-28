from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
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

    machines = relationship("Machine", back_populates="user")
    heartbeats = relationship("Heartbeat", back_populates="user")
    daily_activities = relationship("DailyActivity", back_populates="user")


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_name = Column(String, nullable=False)

    user = relationship("User", back_populates="machines")
    heartbeats = relationship("Heartbeat", back_populates="machine")


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

    user = relationship("User", back_populates="heartbeats")
    machine = relationship("Machine", back_populates="heartbeats")


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    total_active_seconds = Column(Integer, default=0)
    project_worked_on = Column(JSON)

    user = relationship("User", back_populates="daily_activities")
