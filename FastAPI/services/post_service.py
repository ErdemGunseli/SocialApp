import os
from typing import List

from fastapi import HTTPException, File, UploadFile, status as st

from dependencies import db_dependency, user_dependency
from schemas import CreatePostRequest, UpdatePostRequest
from models import Post, Image, Vote
from security import check_for_malware
from enums import VoteType, Order
from config import read_config
from services.utils import order_query
from services.image_service import create_image


def verify_post_ownership(user: user_dependency, post: Post) -> None:
    if post.user_id != user.id:
        raise HTTPException(status_code=st.HTTP_403_FORBIDDEN, detail="Access unauthorized")


def create_post(db: db_dependency, user: user_dependency, post_data: CreatePostRequest) -> Post:
    # If the post is in response to another, ensuring that it exists:
    if post_data.response_to is not None: get_post(db, post_data.response_to)

    new_post = Post(**post_data.dict(), user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_post(db: db_dependency, post_id: int) -> Post:
    # Retrieving the post based on its ID:
    post = db.query(Post).filter(Post.id == post_id).first()

    # Ensuring the post exists:
    if post is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_posts(db: db_dependency, user_id: int = None, title: str = None, response_to: int = None, order_by: Order = Order.DATE, show_comments=False) -> list[Post]:
    query = db.query(Post)

    if user_id: query = query.filter(Post.user_id == user_id)
    # The 'ilike' function allows for case insensitive search, and the '%' signs are wildcards:
    if title: query = query.filter(Post.title.ilike(f"%{title}%"))
    if response_to: query = query.filter(Post.response_to == response_to)
    if not show_comments: query = query.filter(Post.response_to == None)

    return order_query(query, order_by).all()


def update_post(db: db_dependency,user: user_dependency, post_id: int, post_data: UpdatePostRequest):
    post = db.query(Post).filter(Post.id == post_id).first()
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
            if os.path.exists(image.path): os.remove(image.path)
    except Exception as e:
        print(f"Failed to delete one or more image files: {e}")      

    db.delete(post)
    db.commit()


async def create_post_image(db: db_dependency, user: user_dependency, post_id: int, image: UploadFile = File(...)) -> Image:
    path = await create_image(image)
    post = get_post(post_id)
    verify_post_ownership(user, post)

    image_record = Image(post_id=post_id, path=path)
    db.add(image_record)
    db.commit()

    return image_record


def get_post_images(db: db_dependency, post_id) -> List[Image]:
    return db.query(Post).filter(Post.id == post_id).first().images


def delete_post_image(db: db_dependency, user: user_dependency, post_id: int, image_path: str) -> None:
    post = get_post(db, post_id)
    verify_post_ownership(user, post)

    image = db.query(Image).filter(Image.path == image_path).first()
    if image is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="Image not found")

    try:
        db.delete(image)
        db.commit()

        # If the image exists, deleting it:
        if os.path.exists(image_path): os.remove(image.path)
    except Exception as e:
        print(f"Failed to delete one or more image files: {e}")  
        raise


def vote(db: db_dependency, user: user_dependency, post_id: int, vote_type: VoteType) -> Post:

    post = get_post(db, post_id)
    existing_vote = db.query(Vote).filter((Vote.post_id == post_id) & (Vote.user_id == user.id)).first()

    if existing_vote:
        
        if existing_vote.vote_type == vote_type:
            # If the vote type is the same, deleting it and decreasing counter:
            db.delete(existing_vote)

            if vote_type == VoteType.UP: post.upvote_count -= 1
            else: post.downvote_count -= 1

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

    else:
        # Creating a new vote and increasing the relevant counter by 1:
        # Need to use a new variable since DB objects are assigned by reference:
        new_vote = Vote(post_id=post_id, user_id=user.id, vote_type=vote_type)
        db.add(new_vote)

        if vote_type == VoteType.UP: post.upvote_count += 1
        else: post.downvote_count += 1
    
    db.commit()
    db.refresh(post)
    return post
