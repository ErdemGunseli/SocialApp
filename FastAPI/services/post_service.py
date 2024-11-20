import os
from typing import List, Optional

from fastapi import File, UploadFile, status as st

from dependencies import db_dependency, user_dependency, optional_user_dependency
from schemas import CreatePostRequest, UpdatePostRequest, PostResponse, VoteResponse
from models import Post, Image, User, Vote
from enums import VoteType, Order
from services.utils import order_query
from services.image_service import create_image
from exceptions import PostNotFoundError, UnauthorizedAccessError, ImageNotFoundError


def verify_post_ownership(user: user_dependency, post: Post) -> None:
    if post.user_id != user.id:
        raise UnauthorizedAccessError


# Returning 'PostResponse' instead of 'Post' since the model doesn't include current_user_vote:
def create_post(db: db_dependency, user: user_dependency, post_data: CreatePostRequest) -> PostResponse:
    
    # If the post is a comment, ensuring that the parent post exists:
    if post_data.parent_id is not None: 
        parent_id = post_data.parent_id

        # Adding 1 to the comment counter of all parent posts:
        while parent_id is not None:
            parent = get_post(db, parent_id)
            parent.comment_count += 1
            parent_id = parent.parent_id

    new_post = Post(**post_data.dict(), user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # The user is automatically upvotes their post:
    vote(db, user, new_post.id, VoteType.UP)
    new_post.current_user_vote = VoteType.UP

    return new_post


# Recursively populates the 'current_user_vote' field of the post and comments
def populate_current_user_votes(db: db_dependency, user: user_dependency, post: Post):
    vote = db.query(Vote).filter_by(post_id=post.id, user_id=user.id).first()
    post.current_user_vote = vote.vote_type if vote else None

    for comment in post.comments:
        populate_current_user_votes(db, user, comment)


def get_post(db: db_dependency, post_id: int, user: optional_user_dependency = None) -> PostResponse:
    # Retrieving the post based on its ID:
    post = db.query(Post).filter_by(id=post_id).first()

    # Ensuring the post exists:
    if post is None: raise PostNotFoundError
    if user: populate_current_user_votes(db, user, post)

    return post


def get_posts(db: db_dependency, user: optional_user_dependency = None,  user_id: int = None, user_vote: VoteType = None,
              username: str = None, title: str = None, parent_id: int = None, order_by: Order = Order.DATE, show_comments=False) -> List[PostResponse]:
    
    query = db.query(Post).join(User)

    if user and user_vote:
        # Querying the post_id column of Vote, where vote_type=user_vote
        # 'subquery' allows us to use the result in a different query (is more efficient for this):
        post_ids_subquery = db.query(Vote.post_id).filter(Vote.user_id == user.id, Vote.vote_type == user_vote).subquery()
        
        # 'in_' method works similarly to [post_id for post_id in post_ids]
        query = db.query(Post).filter(Post.id.in_(post_ids_subquery))

        # Slower alternative:
        # votes = db.query(Vote).filter_by(vote_type=user_vote).all()
        # post_ids = set([vote.post_id for vote in votes])
        # query = db.query(Post).filter(Post.id in post_ids)


    if user_id: query = query.filter(Post.user_id == user_id)
    # The 'ilike' function allows for case insensitive search, and the '%' signs are wildcards:
    if username: query = query.filter(User.name.ilike(f"%{username}%"))
    if title: query = query.filter(Post.title.ilike(f"%{title}%"))
    if parent_id: query = query.filter(Post.parent_id == parent_id)

    if not show_comments: query = query.filter(Post.parent_id == None)


    posts = order_query(query, order_by).all()
    
    if user:
        for post in posts:
            populate_current_user_votes(db, user, post)

    return posts


def update_post(db: db_dependency,user: user_dependency, post_id: int, post_data: UpdatePostRequest) -> None:
    post = get_post(db, post_id)
    verify_post_ownership(user, post)

    for key, value in post_data.dict().items():
        setattr(post, key, value)

    db.commit()


def delete_post(db: db_dependency, user: user_dependency, post_id: int) -> None:
    post = get_post(db, post_id)
    verify_post_ownership(user, post)
    
    # Only deleting the images themselves, not the database records (which are cascade deleted):
    try:
        for image in post.images:
            # If the image exists, deleting it:
            if os.path.exists(image.url): os.remove(image.url)
    except Exception as e:
        print(f"Failed to delete one or more image files: {e}")      

    db.delete(post)
    db.commit()


async def create_post_image(db: db_dependency, user: user_dependency, post_id: int, image: UploadFile = File(...)) -> Image:
    url = await create_image(image)
    post = get_post(db, post_id)
    verify_post_ownership(user, post)

    image_record = Image(post_id=post_id, url=url)
    db.add(image_record)
    db.commit()

    return image_record


def get_post_images(db: db_dependency, post_id) -> List[Image]:
    post = get_post(db, post_id)

    return post.images


def delete_post_image(db: db_dependency, user: user_dependency, post_id: int, url: str) -> None:
    post = get_post(db, post_id)
    verify_post_ownership(user, post)

    image = db.query(Image).filter_by(url=url).first()
    if image is None: raise ImageNotFoundError

    try:
        db.delete(image)
        db.commit()

        # If the image exists, deleting it:
        if os.path.exists(url): os.remove(url)
    except Exception as e:
        print(f"Failed to delete one or more image files: {e}")  
        raise


def vote(db: db_dependency, user: user_dependency, post_id: int, vote_type: VoteType) -> VoteResponse:
    post = get_post(db, post_id)
    existing_vote = db.query(Vote).filter_by(post_id=post_id, user_id=user.id).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # If the vote type is the same, deleting it and decreasing counter:
            db.delete(existing_vote)
            if vote_type == VoteType.UP: post.upvote_count -= 1
            else: post.downvote_count -= 1

            # User has removed their vote:
            current_vote = None
        else:
            # If it is the opposite vote type, changing it, updating counters:
            existing_vote.vote_type = vote_type
            if vote_type == VoteType.UP:
                # If the vote was down and changed to up:
                post.upvote_count += 1
                post.downvote_count -= 1
            else:
                post.upvote_count -= 1
                post.downvote_count += 1
            
            # User has changed their vote:
            current_vote = vote_type
    else:
        # Creating a new vote and increasing the relevant counter by 1:
        # Need to use a new variable since DB objects are assigned by reference:
        new_vote = Vote(post_id=post_id, user_id=user.id, vote_type=vote_type)
        db.add(new_vote)
        if vote_type == VoteType.UP: post.upvote_count += 1
        else: post.downvote_count += 1

        # User has added a vote
        current_vote = vote_type
    
    db.commit()
    db.refresh(post)
    post.current_user_vote = current_vote
    return post