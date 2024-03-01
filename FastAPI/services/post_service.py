import os
import uuid
from typing import List

import aiofiles
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, File, UploadFile, status as st

from dependencies import db_dependency, user_dependency
from schemas import CreatePostRequest
from models import Post, Image, Vote
from security import check_for_malware
from enums import VoteType, VoteAction
from config import read_config


# The directory where the images for posts are saved (called when the module is imported from main):
IMAGE_DIRECTORY = read_config("image_directory")

# The image MIME (content) types that are allowed:
IMAGE_MIME_TYPES = read_config("image_mime_types")


def create_post(request: CreatePostRequest, user: user_dependency, db: db_dependency) -> Post:

    # If the post is in response to another, ensuring that it exists:
    if request.response_to is not None: get_post(request.response_to, db)

    new_post = Post(**request.dict(), user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_post(post_id: int, db: db_dependency) -> Post:
    # Retrieving the post based on its ID:
    post = db.query(Post).filter(Post.id == post_id).first()

    # Ensuring the post exists:
    if post is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_all_posts(db: db_dependency) -> List[Post]:
    # Returning a list is a synchronous operation so not calling with await:
    # Since the contents of this function are synchronous, the function itself is not async:
    return db.query(Post).all()


def check_post_ownership(post: Post, user: user_dependency):
    if post.user_id != user.id:
        raise HTTPException(status_code=st.HTTP_403_FORBIDDEN, detail="Access unauthorized")


async def create_image(post_id: int, user: user_dependency, db: db_dependency, image: UploadFile = File(...)) -> dict: 
    image_path = ""
    
    # Checking if the uploaded file is an allowed image type:
    if image.content_type not in IMAGE_MIME_TYPES:
        await image.close()  # Close the file to clean up resources
        raise HTTPException(status_code=st.HTTP_400_BAD_REQUEST, detail="Unsupported file type.")

    # Ensuring that the post exists and belongs to the currently logged in user:
    post = get_post(post_id, db)
    check_post_ownership(post, user)

    try:    
        # Generating a universally unique ID for the image file name:
        image_uuid = uuid.uuid4()

        # os.path.splittext splits the string into two parts (before and after the last dot):
        extension = os.path.splitext(image.filename)[1]
        image_path = os.path.join(IMAGE_DIRECTORY, f"{image_uuid}{extension}")

        # Checking for malware in the image file:
        check_for_malware(image)

        # "wb" is for writing in binary mode, aiofiles allows async operations:
        async with aiofiles.open(image_path, "wb") as saved_image:
            # await is used to not block the event loop when calling async functions:
            content = await image.read()
            await saved_image.write(content)

        new_image = Image(uuid=image_uuid, post_id=post_id, path=image_path)
        db.add(new_image)
        db.commit()
    
        # Returning a relative path:
        return {"path": image_path}
    
    except Exception as e:
        print(f"Error saving image: {e}")

        db.rollback()
        # Deleting the image file if it exists:
        if os.path.exists(image_path): os.remove(image_path)

        # Raising the exception again to be caught by the exception handler (HTTP Exception returned to the client):
        raise

    finally:
        await image.close()
    



def delete_post(post_id: int, user: user_dependency, db: db_dependency) -> None:
    post = get_post(post_id, db)
    check_post_ownership(post, user)
    
    # Important that this is called before deleting the post:
    delete_post_images(post)
    db.delete(post)
    db.commit()


def delete_post_images(post: Post) -> None:
    try:
        for image in post.images:
            # If the image exists, deleting it:
            if os.path.exists(image.path): os.remove(image.path)
    except Exception as e:
        print(f"Failed to delete one or more image files: {e}")    


def vote(post_id: int, vote_type: VoteType, user: user_dependency, db: db_dependency) -> dict:

    post = get_post(post_id, db)
    existing_vote = db.query(Vote).filter((Vote.post_id == post_id) & (Vote.user_id == user.id)).first()
    action = None

    try:
        if existing_vote:
            vote_id = existing_vote.id
            
            if existing_vote.vote_type == vote_type:
                # If the vote type is the same, deleting it and decreasing counter:
                db.delete(existing_vote)
                action = VoteAction.DELETED

                if vote_type == VoteType.UP: post.upvote_count -= 1
                else: post.downvote_count -= 1

            else:
                # If it is the opposite vote type, changing it, updating counters:
                existing_vote.vote_type = vote_type
                action = VoteAction.CHANGED

                if vote_type == VoteType.UP:
                    # If the vote was down and changed to up:
                    post.upvote_count += 1
                    post.downvote_count -= 1
                else:
                    post.upvote_count -= 1
                    post.downvote_count += 1

            db.commit()  

        else:
            # Creating a new vote and increasing the relevant counter by 1:
            # Need to use a new variable since DB objects are assigned by reference:
            new_vote = Vote(post_id=post_id, user_id=user.id, vote_type=vote_type)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            vote_id = new_vote.id
            action = VoteAction.ADDED

            if vote_type == VoteType.UP: post.upvote_count += 1
            else: post.downvote_count += 1

            db.commit()

        return {
                "id": vote_id,
                "vote_type": vote_type,
                "action": action,
                "upvote_count": post.upvote_count,
                "downvote_count": post.downvote_count
                }

    except SQLAlchemyError as e:
        db.rollback()
        raise e
