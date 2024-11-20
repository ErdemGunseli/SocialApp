from typing import List, Optional

from fastapi import APIRouter, Path, File, Query, UploadFile, status as st
from starlette.requests import Request

from main import app
from services import post_service as ps
from schemas import CreatePostRequest, UpdatePostRequest, PostResponse, VoteResponse, ImageResponse
from dependencies import db_dependency, user_dependency, optional_user_dependency
from enums import Order, VoteType


router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostResponse, status_code=st.HTTP_201_CREATED)
# Using stricter rate limiting to prevent spam posts:
@app.state.limiter.limit("10/minute, 20/hour, 50/day")
async def create_post(db: db_dependency, user: user_dependency, post_data: CreatePostRequest, request: Request):
    return ps.create_post(db, user, post_data)


@router.get("/{post_id}", response_model=PostResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("100/minute")
# User is optional, but providing it allows for additional data to be returned with the request:
async def read_post(db: db_dependency, request: Request, user: optional_user_dependency, post_id: int = Path(ge=0)):
    return ps.get_post(db, post_id, user=user)


@router.get("/", response_model=List[PostResponse], status_code=st.HTTP_200_OK)
@app.state.limiter.limit("100/minute")
async def read_posts(db: db_dependency, user: optional_user_dependency, request: Request,
                        user_id: int = Query(default=None, ge=0), user_vote: VoteType = Query(default=None),
                        username: str = Query(None), title: str = Query(None), parent_id: int = Query(None), 
                        order_by: Order = Query(Order.DATE), show_comments: bool = Query(False)):
    return ps.get_posts(db, user=user, user_id=user_id, user_vote=user_vote, username=username, title=title, parent_id=parent_id, 
                        order_by=order_by, show_comments=show_comments)


@router.put("/{post_id}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("10/minute")
async def update_post(db: db_dependency, user: user_dependency, post_data: UpdatePostRequest, request: Request, post_id: int = Path(ge=0)):
    ps.update_post(db, user, post_id, post_data)


@router.delete("/{post_id}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("10/minute")
async def delete_post(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0)):
    ps.delete_post(db, user, post_id)


@router.post("/{post_id}/image/", response_model=ImageResponse, status_code=st.HTTP_201_CREATED)
@app.state.limiter.limit("10/minute")
async def create_post_image(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), image: UploadFile = File(...)):
    return await ps.create_post_image(db, user, post_id, image)


@router.get("/{post_id}/images", response_model=List[ImageResponse], status_code=st.HTTP_200_OK)
@app.state.limiter.limit("100/minute")
async def read_post_images(db: db_dependency, request: Request, post_id: int = Path(ge=0)):
    return ps.get_post_images(db, post_id)


@router.delete("/{post_id}/image/{url:path}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("10/minute")
async def delete_post_image(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), url: str = Path(...)):
    ps.delete_post_image(db, user, post_id, url)


@router.post("/{post_id}/vote/", response_model=VoteResponse, status_code=st.HTTP_201_CREATED)
@app.state.limiter.limit("30/minute")
async def vote(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), vote_type: VoteType = Query(...)):
    return ps.vote(db, user, post_id, vote_type)
