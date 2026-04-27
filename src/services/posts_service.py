from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database.session import get_db
from src.models.models import Post
from src.schemas.posts_models import Post as PostSchema, PostUpdate


def get_all(db: Session, limit: int = 20, offset: int = 0) -> List[Post]:
    return db.query(Post).offset(offset).limit(limit).all()


def get_latest(db: Session, limit: int = 10, offset: int = 0) -> List[Post]:
    return db.query(Post).order_by(Post.date.desc()).offset(offset).limit(limit).all()


def get_byid(post_id: int, db: Session) -> Post:
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_by_username(username: str, db: Session) -> List[Post]:
    return db.query(Post).filter(Post.user == username).order_by(Post.date.desc()).all()


def create_post(post: PostSchema, current_user, db: Session) -> Post:
    new_post = Post(**post.model_dump(), user=current_user.username)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(post_id: int, updated_value: PostUpdate, current_user, db: Session) -> Post:
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    for key, value in updated_value.model_dump(exclude_none=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def delete_post(post_id: int, current_user, db: Session):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
