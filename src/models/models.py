from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from src.database.session import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    subreddit = Column(String, nullable=False)
    user = Column("user", String, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
