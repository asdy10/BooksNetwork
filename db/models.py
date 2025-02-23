from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func
import uuid
from datetime import datetime, timedelta
import sqlalchemy as sa


class Base(DeclarativeBase):
    id = sa.Column(sa.VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = sa.Column(sa.DateTime, default=func.now())
    updated_at = sa.Column(sa.DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "user"
    first_name = sa.Column(sa.Text, nullable=True)
    last_name = sa.Column(sa.Text, nullable=True)
    email = sa.Column(sa.Text)
    hashed_password = sa.Column(sa.Text)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    __tablename__ = "book"
    title = sa.Column(sa.VARCHAR(200))
    description = sa.Column(sa.Text, nullable=True)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Review(Base):
    __tablename__ = "review"
    book_id = sa.Column(sa.VARCHAR(36))
    user_id = sa.Column(sa.VARCHAR(36))
    text = sa.Column(sa.Text)
    rate = sa.Column(sa.Integer)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Message(Base):
    __tablename__ = "message"
    from_user = sa.Column(sa.VARCHAR(36))
    to_user = sa.Column(sa.VARCHAR(36))
    text = sa.Column(sa.Text)
    is_read = sa.Column(sa.Boolean, default=False)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
