from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    data_sessions = relationship("DataSession", back_populates="user")

class DataSession(Base):
    __tablename__ = "data_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data_location = Column(String)  # Path to stored CSV file
    analysis_details = Column(Text)  # User's text input about the data
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="data_sessions") 