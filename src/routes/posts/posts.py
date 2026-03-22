from fastapi import APIRouter, Response, status
from src.pydantic_models import posts_models as posts_models
from src.services import posts_service as posts
from typing import List, Optional

router = APIRouter(
    prefix="/r",
    tags=['Subreddit']
)


@router.get("/",status_code=status.HTTP_200_OK, response_model=List[posts_models.Post])
def get_posts():
    return posts.get_all()
@router.get("/latest", status_code=status.HTTP_200_OK, response_model=List[posts_models.Post])
def get_latest_posts():
    return posts.get_latest()

@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=posts_models.PostFull)
def get_post_by_id(post_id: int):
    return posts.get_byid(post_id)

