from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    alias = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    visited_at = Column(DateTime, default=datetime.now)
    client_ip = Column(String)
    user_agent = Column(String)
