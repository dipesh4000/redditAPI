from fastapi import FastAPI
from src.posts import posts

app = FastAPI(title="Reddit API", 
            description="A simple API for Reddit",
            version="1.0.0")

app.include_router(posts.router)



@app.get("/")
def homepage():
    return {"message": "Welcome to Reddit!", "quote": "The heart of the Internet", "status": "success"}

@app.get("/signup")
def create_new_user():
    return "user created"

@app.get("/login")
def user_login():
    return "Succesfuly logged in"