from pydantic import BaseModel

class post(BaseModel):
    title: str
    content: str
    subreddit: str
    user: str