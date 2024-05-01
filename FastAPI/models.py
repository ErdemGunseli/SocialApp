from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, UniqueConstraint

from database import Base
from enums import Role, VoteType


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    # "back_populates" provides bidirectional relationship where User can access 'posts' and each Post can access 'user'
    posts = relationship("Post", back_populates="user")

    profile_image = relationship("Image", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Post(Base):
    # Posts and responses (essentially comments) have the same requirements.
    # They both need votes and images (so new tables or relationships would be needed for those).
    # Therefore, it makes most sense to store both in the same table.

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # Responses do not have a title:
    title = Column(String, nullable=True, index=True)
    body = Column(String)
    
    # If the post is a response, this is the ID of the parent:
    response_to = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)

    # Keeping upvote and downvote counters here so they are not counted each time:
    upvote_count = Column(Integer, index=True, default=0)
    downvote_count = Column(Integer, index=True, default=0)
    created_at = Column(DateTime, index=True, server_default=func.now())

    user = relationship("User", back_populates="posts")

    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")

    # Using self-referencing relationship for the hierarchical structure of posts/responses:
    responses = relationship("Post", cascade="all, delete-orphan", backref=backref("parent", remote_side=[id]))
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    # Only has a value for profile images:
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    # Only has a value for post images:
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)
    path = Column(String, index=True)
    uploaded_at = Column(DateTime, server_default=func.now())

    # Specifying that owner_id is a foreign key here since we do not know which table it relates to:
    user = relationship("User", back_populates="profile_image")
    post  = relationship("Post", back_populates="images")


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)

    post = relationship("Post", back_populates="votes")
    # Setting a constraint that the combination of post_id and user_id should be unique.
    # Do not remove the comma, table args must be a tuple:
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='unique_post_user_vote'), )
