import os

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, UniqueConstraint

from database import Base
from enums import Role, VoteType

BASE_URL = 'http://localhost:8000'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    # "back_populates" provides bidirectional relationship where User can access 'posts' and each Post can access 'user'
    posts = relationship("Post", back_populates="author")

    profile_image = relationship("Image", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Post(Base):
    # Posts and comments have the same requirements.
    # They both need votes and images (so new tables or relationships would be needed for those).
    # Therefore, it makes most sense to store both in the same table.

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # Comments may not have a title:
    title = Column(String, nullable=True, index=True)
    body = Column(String)
    
    # If the post is a comment, this is the ID of the parent:
    parent_id = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)  # FIXME: CHANGED

    # Keeping  counters here so they are not counted each time:
    comment_count = Column(Integer, default=0)
    upvote_count = Column(Integer, index=True, default=0)
    downvote_count = Column(Integer, default=0)
    created_at = Column(DateTime, index=True, server_default=func.now())


    # The user object who created the post: 
    author = relationship("User", back_populates="posts")

    # Sorting the images by their timestamp, so no need to re-order:
    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")


    # Using self-referencing relationship for the hierarchical structure of posts/comments:
    comments = relationship("Post", cascade="all, delete-orphan", backref=backref("parent", remote_side=[id]))  # FIXME: CHANGED
    
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    # Only has a value for profile images:
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    # Only has a value for post images:
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)
    url = Column(String, index=True)
    uploaded_at = Column(DateTime, server_default=func.now(), index=True)

    user = relationship("User", back_populates="profile_image")
    post = relationship("Post", back_populates="images")

    @property
    def full_url(self):
        if not self.url.startswith("http"):
            full_url = f"{BASE_URL}/{self.url}"
            print(f"Constructed full URL: {full_url}")  # Debugging line
            return full_url
        return self.url


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False) # TODO: CHANGE TO 'type'

    post = relationship("Post", back_populates="votes")
    # Setting a constraint that the combination of post_id and user_id should be unique.
    # Do not remove the comma, table args must be a tuple:
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='unique_post_user_vote'), )