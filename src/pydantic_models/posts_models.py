from pydantic import BaseModel
from datetime import datetime, time

class Post(BaseModel):
    title: str
    content: str
    subreddit: str
    user: str


class PostFull(Post):
    post_id: int
    created_at: time