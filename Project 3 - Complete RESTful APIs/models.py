"""Database models for the Todo application."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Users(Base):  # pylint: disable=too-few-public-methods
    """Users model representing a user entity in the application."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Todos(Base):  # pylint: disable=too-few-public-methods
    """Todos model representing a todo entity in the application."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
