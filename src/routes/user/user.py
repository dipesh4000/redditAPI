from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.services import posts_service
from src.schemas import posts_models
from src.services.user_service import get_current_user
from src.database.session import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{username}/posts", status_code=status.HTTP_200_OK, response_model=List[posts_models.PostFull])
def get_user_posts(username: str, db: Session = Depends(get_db)):
    return posts_service.get_by_username(username, db)


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=posts_models.PostFull)
def post(body: posts_models.Post, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return posts_service.create_post(body, current_user, db)


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=posts_models.PostFull)
def update(post_id: int, body: posts_models.PostUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return posts_service.update_post(post_id, body, current_user, db)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    posts_service.delete_post(post_id, current_user, db)
