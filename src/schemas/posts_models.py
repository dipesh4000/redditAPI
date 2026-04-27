from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    subreddit: str


class PostFull(Post):
    post_id: int
    date: datetime
    user: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    subreddit: Optional[str] = None
