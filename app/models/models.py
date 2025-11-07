import datetime

from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Boolean,
    Column,
    Date,
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

    # Relationships
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
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    is_active = Column(Boolean, default=True)

    # Relationship
    user = relationship("User", back_populates="api_keys")


class Heartbeat(Base):
    __tablename__ = "heartbeats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    entity = Column(String, nullable=False)
    alternate_project = Column(String)
    project_folder = Column(String)
    project_root_count = Column(Integer)
    language = Column(String)
    time = Column(TIMESTAMP, nullable=False)
    is_write = Column(Boolean, default=False)
    lineno = Column(Integer)
    cursorpos = Column(Integer)
    lines_in_file = Column(Integer)
    line_changes = Column(Integer)
    is_unsaved_entity = Column(Boolean, default=False)

    # Relationship
    user = relationship("User", back_populates="heartbeats")


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    total_active_seconds = Column(Integer, default=0)
    total_files_edited = Column(Integer, default=0)
    total_projects = Column(Integer, default=0)
    total_languages = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))

    # Relationships
    user = relationship("User", back_populates="daily_activities")
    project_activities = relationship(
        "DailyProjectActivity",
        back_populates="daily_activity",
        cascade="all, delete-orphan",
    )
    language_activities = relationship(
        "DailyLanguageActivity",
        back_populates="daily_activity",
        cascade="all, delete-orphan",
    )
    file_activities = relationship(
        "DailyFileActivity",
        back_populates="daily_activity",
        cascade="all, delete-orphan",
    )


class DailyProjectActivity(Base):
    __tablename__ = "daily_project_activity"

    id = Column(Integer, primary_key=True, index=True)
    daily_activity_id = Column(Integer, ForeignKey("daily_activity.id"), nullable=False)
    project_name = Column(String, nullable=False)
    total_seconds = Column(Integer, default=0)
    files_edited = Column(Integer, default=0)

    daily_activity = relationship("DailyActivity", back_populates="project_activities")


class DailyLanguageActivity(Base):
    __tablename__ = "daily_language_activity"

    id = Column(Integer, primary_key=True, index=True)
    daily_activity_id = Column(Integer, ForeignKey("daily_activity.id"), nullable=False)
    language = Column(String, nullable=False)
    total_seconds = Column(Integer, default=0)

    daily_activity = relationship("DailyActivity", back_populates="language_activities")


class DailyFileActivity(Base):
    __tablename__ = "daily_file_activity"

    id = Column(Integer, primary_key=True, index=True)
    daily_activity_id = Column(Integer, ForeignKey("daily_activity.id"), nullable=False)
    entity = Column(String, nullable=False)
    project = Column(String)
    total_seconds = Column(Integer, default=0)
    total_line_changes = Column(Integer, default=0)

    daily_activity = relationship("DailyActivity", back_populates="file_activities")
