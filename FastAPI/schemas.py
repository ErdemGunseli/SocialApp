import datetime
from typing import Optional, List

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



class ImageResponse(BaseModel):
    url: str

    @classmethod
    def from_orm(cls, image):
        return cls(url=image.full_url)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str

    # Including this (even though it is not a part of the user record)
    # to reduce the number of API calls:
    profile_image: Optional[ImageResponse] = None

    class Config:
        from_attributes = True


class PrivateUserResponse(UserResponse):
    # Only used for the endpoint that returns the currently logged in user:

    email: EmailStr
    role: Role


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    # from_attributes is false because data will be provided as a dictionary, not from the db.


class CreatePostRequest(BaseModel):
     # user_id is based on the current user
    title: Optional[str] = Field(max_length=1000)
    body: str = Field(max_length=5000)
    # None is the default value:
    parent_id: Optional[int] = None


class UpdatePostRequest(BaseModel):
    # The parent_id field cannot be updated:
    title: Optional[str] = Field(max_length=1000)
    body: str = Field(max_length=5000)



class PostResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    body: str

    parent_id: Optional[int]
    comment_count: int
    # Using a string to be able to refer to the class before it is defined:
    comments: Optional[List["PostResponse"]]

    upvote_count: int
    downvote_count: int
    created_at: datetime.datetime

    # The images associated to the post:
    images: List[ImageResponse]

    # Returning the details of the author to reduce the number of API calls:
    author: UserResponse

    current_user_vote: Optional[VoteType] = None

    class Config: 
        from_attributes = True


class CreateVoteRequest(BaseModel):
    # post_id and user_id obtained from url param and dependency
    type: VoteType


class VoteResponse(BaseModel):
    current_user_vote: Optional[VoteType] = None
    upvote_count: int
    downvote_count: int