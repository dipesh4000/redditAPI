from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.orm import Session
from src.schemas import posts_models
from src.services import posts_service
from src.database.session import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[posts_models.PostFull])
def get_posts(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return posts_service.get_all(db, limit, offset)


@router.get("/latest", status_code=status.HTTP_200_OK, response_model=List[posts_models.PostFull])
def get_latest_posts(limit: int = Query(10, ge=1, le=50), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return posts_service.get_latest(db, limit, offset)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=posts_models.PostFull)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return posts_service.get_byid(post_id, db)
