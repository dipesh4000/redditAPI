from fastapi import FastAPI
from src.posts import post

app = FastAPI(title="Reddit API", 
            description="A simple API for Reddit",
            version="1.0.0")

app.include_router(post.router)



@app.get("/")
def homepage():
    return {"message": "Welcome to Reddit!", "quote": "The heart of the Internet", "status": "success"}

