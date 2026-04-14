from fastapi import APIRouter, status, HTTPException, Depends
from src.services import posts_service
from src.schemas import posts_models
from src.services.user_service import get_current_user
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{username}/posts", status_code=status.HTTP_200_OK, response_model=List[posts_models.PostFull])
def get_user_posts(username: str):
    return posts_service.get_by_username(username)


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=posts_models.PostFull)
def post(body: posts_models.Post, current_user=Depends(get_current_user)):
    return posts_service.create_post(body, current_user)


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=posts_models.PostFull)
def update(post_id: int, body: posts_models.PostUpdate, current_user=Depends(get_current_user)):
    return posts_service.update_post(post_id, body, current_user)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: int, current_user=Depends(get_current_user)):
    posts_service.delete_post(post_id, current_user)
