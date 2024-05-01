import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from enums import Role, VoteType


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=6, max_length=100)


class UpdateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(max_length=254)


class UpdateUserPasswordRequest(BaseModel):
    old_password: str = Field(min_length=6, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role

    # Pydantic models normally expect data in the form of dictionaries.
    # We have objects, so setting ORM mode to true:
    # In Pydantic version 2, "orm_mode" has been renamed to "from_attributes"
    class Config: from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    # from_attributes is false because data will be provided as a dictionary, not from the db.


class CreatePostRequest(BaseModel):
     # user_id is based on the current user
    title: Optional[str] = Field(max_length=1000)
    body: str = Field(max_length=5000)
    # None is the default value:
    response_to: Optional[int] = None


class UpdatePostRequest(BaseModel):
    # The response_to field cannot be updated:
    title: Optional[str] = Field(max_length=1000)
    body: str = Field(max_length=5000)


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    body: str
    response_to: Optional[int]
    upvote_count: int
    downvote_count: int
    created_at: datetime.datetime

    class Config: from_attributes = True


class ImageResponse(BaseModel):
    path: str


class CreateVoteRequest(BaseModel):
    # post_id and user_id obtained from path param and dependency
    type: VoteType


class VoteResponse(BaseModel):
    upvote_count: int
    downvote_count: int
