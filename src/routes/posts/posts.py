from fastapi import APIRouter, status, HTTPException
from src.pydantic_models import posts_models as posts_models
from src.services import posts_service as posts_service
from typing import List

router = APIRouter(
    prefix="/r",
    tags=['Subreddit']
)


@router.get("/",status_code=status.HTTP_200_OK, response_model=List[posts_models.Post])
def get_posts():
            # 'raise' stops execution and sends the 502 error immediately
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Specify the subreddit"
    )
@router.get("/latest", status_code=status.HTTP_200_OK, response_model=List[posts_models.Post])
def get_latest_posts():
    return posts_service.get_latest()

@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=posts_models.PostFull)
def get_post_by_id(post_id: int):
    return posts_service.get_byid(post_id)

