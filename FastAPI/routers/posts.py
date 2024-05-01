from typing import List

from fastapi import APIRouter, Path, File, Query, UploadFile, status as st
from starlette.requests import Request

from main import app
from services import post_service as ps
from schemas import CreatePostRequest, UpdatePostRequest, PostResponse, VoteResponse, ImageResponse
from dependencies import db_dependency, user_dependency
from enums import Order, VoteType


router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostResponse, status_code=st.HTTP_201_CREATED)
# Using stricter rate limiting to prevent spam posts:
@app.state.limiter.limit("20/minute, 60/hour, 600/day")
async def create_post(db: db_dependency, user: user_dependency, post_data: CreatePostRequest, request: Request):
    return ps.create_post(db, user, post_data)


@router.get("/{post_id}", response_model=PostResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("")
async def read_post(db: db_dependency, request: Request, post_id: int = Path(ge=0)):
    return ps.get_post(db, post_id)


@router.get("/", response_model=List[PostResponse], status_code=st.HTTP_200_OK)
@app.state.limiter.limit("")
async def read_posts(db: db_dependency, request: Request,
                         user_id: int = Query(default=None, ge=0), title: str = Query(None), response_to: int = Query(None), 
                         order_by: Order = Query(Order.DATE), show_comments: bool = Query(False)):
    return ps.get_posts(db, user_id=user_id, title=title, response_to=response_to, order_by=order_by, show_comments=show_comments)


@router.put("/{post_id}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("")
async def update_post(db: db_dependency, user: user_dependency, post_data: UpdatePostRequest, request: Request, post_id: int = Path(ge=0)):
    ps.update_post(db, user, post_id, post_data)


@router.delete("/{post_id}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("")
async def delete_post(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0)):
    ps.delete_post(db, user, post_id)


@router.post("/{post_id}/image/", response_model=ImageResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("")
async def create_post_image(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), image: UploadFile = File(...)):
    ps.create_post_image(db, user, post_id, image)


@router.get("/{post_id}/images", response_model=List[ImageResponse], status_code=st.HTTP_200_OK)
@app.state.limiter.limit("")
async def read_post_images(db: db_dependency, request: Request, post_id: int = Path(ge=0)):
    ps.get_post_images(db, post_id)


@router.delete("/{post_id}/image/{image_path: path}", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("")
async def delete_post_image(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), image_path: str = Path(...)):
    ps.delete_post_image(db, user, post_id, image_path)


@router.post("/{post_id}/vote/", response_model=VoteResponse, status_code=st.HTTP_201_CREATED)
@app.state.limiter.limit("")
async def vote(db: db_dependency, user: user_dependency, request: Request, post_id: int = Path(ge=0), vote_type: VoteType = Query(...)):
    return ps.vote(db, user, post_id, vote_type)
