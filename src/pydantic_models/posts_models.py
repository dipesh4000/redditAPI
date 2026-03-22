from pydantic import BaseModel
from datetime import datetime

class post(BaseModel):
    title: str
    content: str
    subreddit: str
    user: str


class postfull(post):
    post_id: int
    created_at: datetime
