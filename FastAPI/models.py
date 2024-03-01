import uuid

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, UniqueConstraint

from database import Base
from enums import Role, VoteType

# TODO: Store length constraints in a separate JSON file and enforce 
# on the database level as well (in addition to Pydantic)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    posts = relationship('Post', back_populates="user")

    # TODO: Add description and profile image.


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
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    user = relationship('User', back_populates="posts")
    # When the post is deleted, all images that are/were associated to the post should be deleted as well:
    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")

    # Using self-referencing relationship for the hierarchical structure of posts/responses:
    responses = relationship('Post', cascade="all, delete-orphan", backref=backref('parent', remote_side=[id]))

    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    # "as_uuid" determines whether it should be stored as python UUID objects or strings:
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    path = Column(String)
    uploaded_at = Column(DateTime, server_default=func.now())
    # TODO: For now, order based on upload time. Introduce attribute later.

    post = relationship("Post", back_populates="images")



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
