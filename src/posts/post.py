from fastapi import APIRouter, Response, status
from src.posts import pydantic_models

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= pydantic_models.post)
def get_posts():
    return {"title": "USA attacked IRAN", "content": "Yesterday blah blah", "subreddit": "worldnews", "user": "john_doe"}

@router.get("/latest", response_model= pydantic_models.post)
def get_latest_posts():
    return {"message": "List of latest Reddit posts", "status": "success"}

@router.get("/{post_id}", response_model= pydantic_models.postfull)
def get_post_by_id(post_id: int):
    return {"message": f"Details of Reddit post with ID {post_id}", "status": "success"}

