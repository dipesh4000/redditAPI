from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    subreddit: str


class PostFull(Post):
    post_id: int
    created_at: time


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    subreddit: Optional[str] = None
    user: Optional[str] = None
