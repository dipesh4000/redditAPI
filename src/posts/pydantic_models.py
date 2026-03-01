from pydantic import BaseModel
from datetime import datetime

class post(BaseModel):
    title: str
    content: str
    subreddit: str
    user: str


class postfull(post):
    id: int
    created_at: datetime
