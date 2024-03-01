from typing import List

from fastapi import APIRouter, Path, File, UploadFile, status as st, HTTPException

from services import post_service as ps
from schemas import CreatePostRequest, PostResponse, VoteRequest, VoteResponse, ImageResponse
from dependencies import db_dependency, user_dependency


router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostResponse, status_code=st.HTTP_201_CREATED)
async def create_post(request: CreatePostRequest, user: user_dependency, db: db_dependency):
    return ps.create_post(request, user, db)


@router.get("/", response_model=List[PostResponse], status_code=st.HTTP_200_OK)
async def read_all_posts(db: db_dependency):
    return ps.get_all_posts(db)


@router.delete("/{post_id}", status_code=st.HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, db: db_dependency, post_id: int = Path(ge=0)):
    return ps.delete_post(post_id, user, db)


@router.post("/{post_id}/image", response_model=ImageResponse, status_code=st.HTTP_201_CREATED)
async def create_image(user: user_dependency, db: db_dependency, image: UploadFile = File(...), post_id: int = Path(ge=0)):
    return await ps.create_image(post_id, user, db, image)



@router.post("/{post_id}/vote/", response_model=VoteResponse, status_code=st.HTTP_201_CREATED)
async def vote(request: VoteRequest, user: user_dependency, db: db_dependency, post_id: int = Path(ge=0)):
    return ps.vote(post_id, request.type, user, db)