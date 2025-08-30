from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

like_table = Table(
    'likes',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('post_id', ForeignKey('posts.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    liked_posts = relationship("Post", secondary=like_table, back_populates="liked_by")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    tag = Column(String, index=True)
    liked_by = relationship("User", secondary=like_table, back_populates="liked_posts")